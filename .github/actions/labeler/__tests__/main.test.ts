import {
  extractLabels,
  getName,
  getChecked,
  formatStrArray,
  validateEnums,
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

  it(validateEnums.name, () => {
    expect(validateEnums('a', 'b', ['b'])).toBeUndefined();

    const f = (): void => {
      validateEnums('a', 'b', ['c', 'd']);
    };
    expect(f).toThrow(new Error('`a` must be one of ["c", "d"], but got "b"'));
  });
});
