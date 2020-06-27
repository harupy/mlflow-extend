import {
  extractLabels,
  getName,
  getChecked,
  formatStrArray,
  validateEnum,
} from '../src/main';

describe('main', (): void => {
  it(extractLabels.name, (): void => {
    const body = [
      '- [] `a`: a',
      '- [ ] `b`: b',
      '- [x] `c`: c',
      '- [ x] `d`: d]',
      '- [X] `e`: e]',
      '- [ X] `f`: f]',
    ].join('\n');
    const labelPattern = '- \\[([ xX]*)\\] ?`(.+?)`';
    expect(extractLabels(body, labelPattern)).toEqual([
      { name: 'a', checked: false },
      { name: 'b', checked: false },
      { name: 'c', checked: true },
      { name: 'd', checked: true },
      { name: 'e', checked: true },
      { name: 'f', checked: true },
    ]);
  });

  it(getName.name, (): void => {
    expect(getName({ name: 'a' })).toEqual('a');
  });

  it(getChecked.name, (): void => {
    expect(getChecked({ checked: true })).toEqual(true);
  });

  it(formatStrArray.name, () => {
    expect(formatStrArray(['a', 'b', 'c'])).toEqual('- a\n- b\n- c\n');
    expect(formatStrArray([])).toEqual('');
  });

  it(validateEnum.name, () => {
    enum E1 {
      B = 'b',
    }
    expect(validateEnum('a', 'b' as string, E1)).toBeUndefined();

    enum E2 {
      C = 'c',
      D = 'd',
    }
    const f = (): void => {
      validateEnum('a', 'b' as string, E2);
    };
    expect(f).toThrow(new Error("`a` must be one of ['c', 'd'], but got 'b'"));
  });
});
