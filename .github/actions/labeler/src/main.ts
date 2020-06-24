import * as core from '@actions/core';

export function sample(): string {
  return 'sample';
}

async function run(): Promise<void> {
  try {
    // const token: string = core.getInput('github-token');
    console.log('hello');
  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
