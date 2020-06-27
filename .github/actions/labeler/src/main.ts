import * as core from '@actions/core';
import * as github from '@actions/github';
import * as types from '@octokit/types';

type Label = {
  name: string;
  checked: boolean;
};

/**
 * Extract `checked` value from an object
 * @param body string that contains labels
 * @param labelPattern regular expression to use to find labels
 * @returns labels (list of { name: string; checked: boolean; })
 * 
 * @example
 * > const body = '- [ ] `a`\n- [x] `b`'
 * > const labelPattern = '- \\[([ xX]*)\\] ?`(.+?)`'
 * > extractLabels(body, labelPattern)
 * [ { name: 'a', checked: false }, { name: 'b', checked: true } ]
 */
export function extractLabels(body: string, labelPattern: string): Label[] {
  function helper(regex: RegExp, labels: Label[] = []): Label[] {
    const res = regex.exec(body);
    if (res) {
      const checked = res[1].trim().toLocaleLowerCase() === 'x';
      const name = res[2].trim();
      return helper(regex, [...labels, { name, checked }]);
    }
    return labels;
  }
  return helper(new RegExp(labelPattern, 'gm'));
}

/**
 * Get `name` property from an object
 * @param obj object that has `name` property
 * @returns value of `name` property
 *
 * @example
 * > getName({ name: 'a' })
 * 'a'
 */
export function getName({ name }: { name: string }): string {
  return name;
}

/**
 * Get `checked` property from an object
 * @param obj object that has `checked` property
 * @returns value of `checked` property
 *
 * @example
 * > getChecked({ checked: true })
 * true
 */
export function getChecked({ checked }: { checked: boolean }): boolean {
  return checked;
}

/**
 * Format a string array into a list
 * @param strArray string array
 * @returns string that represents a list
 *
 * @example
 * > toListStr(["a", "b"])
 * - a
 * - b
 */
export function formatStrArray(strArray: string[]): string {
  if (strArray.length === 0) {
    return '';
  }
  return strArray.map(s => `- ${s}`).join('\n') + '\n';
}

/**
 * Validate an enum value
 * @param name name of the variable to check
 * @param val value to check
 * @param enums acceptable values
 *
 * @example
 * > validateEnums('a', 'b', ['c', 'd'])
 * Uncaught Error: `a` must be one of ['c', 'd'], but got 'b'
 */
export function validateEnums<T>(name: T, val: T, enums: T[]): never | void {
  if (!enums.includes(val)) {
    const wrap = (s: T): string => `'${s}'`;
    const joined = enums.map(wrap).join(', ');
    throw new Error(
      `\`${name}\` must be one of [${joined}], but got ${wrap(val)}`,
    );
  }
}

async function main(): Promise<void> {
  try {
    const token = core.getInput('repo-token', { required: true });
    const labelPattern = core.getInput('label-pattern', { required: true });
    const q = core.getInput('quiet', { required: true });

    validateEnums('quiet', q, ['true', 'false']);
    const quiet = q === 'true';

    const octokit = github.getOctokit(token);
    const { repo, owner } = github.context.repo;

    // Iterate over all the open issues and pull requests
    for await (const page of octokit.paginate.iterator(
      octokit.issues.listForRepo,
      { owner, repo },
    )) {
      for (const issue of page.data) {
        /*
          For each issue and pull request, does the following:
          1. Extract labels from the description.
          2. Remove unchecked labels if they are already attached.
          3. Add checked labels if they are NOT attached.
        */

        const {
          body,
          number: issue_number,
          html_url,
        } = issue as types.IssuesGetResponseData;

        if (!quiet) {
          console.log(`<<< ${html_url} >>>`);
        }

        // Labels already attached on the PR
        const labelsOnIssueResp = await octokit.issues.listLabelsOnIssue({
          owner,
          repo,
          issue_number,
        });
        const labelsOnIssue = labelsOnIssueResp.data.map(getName);

        // Labels registered in the repository
        const labelsForRepoResp = await octokit.issues.listLabelsForRepo({
          owner,
          repo,
        });
        const labelsForRepo = labelsForRepoResp.data.map(getName);

        // Labels in the description
        const labels = extractLabels(body, labelPattern).filter(({ name }) =>
          // Remove labels that are not registered in the repository.
          labelsForRepo.includes(name),
        );

        if (labels.length === 0) {
          if (!quiet) {
            console.log('No labels found');
          }
          return;
        }

        if (!quiet) {
          console.log('Checked labels:');
          console.log(formatStrArray(labels.filter(getChecked).map(getName)));
        }

        // Remove unchecked labels
        const labelsToRemove = labels
          .filter(
            ({ name, checked }) => !checked && labelsOnIssue.includes(name),
          )
          .map(getName);

        if (!quiet) {
          console.log('Labels to remove:');
          console.log(formatStrArray(labelsToRemove));
        }

        if (labelsToRemove.length > 0) {
          labelsToRemove.forEach(async name => {
            await octokit.issues.removeLabel({
              owner,
              repo,
              issue_number,
              name,
            });
          });
        }

        // Add checked labels
        const labelsToAdd = labels
          .filter(
            ({ name, checked }) => checked && !labelsOnIssue.includes(name),
          )
          .map(getName);

        if (!quiet) {
          console.log('Labels to add:');
          console.log(formatStrArray(labelsToAdd));
        }

        if (labelsToAdd.length > 0) {
          await octokit.issues.addLabels({
            owner,
            repo,
            issue_number,
            labels: labelsToAdd,
          });
        }
      }
    }
  } catch (error) {
    core.setFailed(error.message);
  }
}

main();
