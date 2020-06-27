import {
  extractLabels,
  getName,
  getChecked,
  logAsList,
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

  it(logAsList.name, () => {
    const consoleLogSpy = jest.spyOn(console, 'log').mockImplementation();
    logAsList(['a', 'b', 'c']);
    logAsList([]);

    expect(consoleLogSpy).toHaveBeenCalledTimes(2);
    expect(consoleLogSpy).toHaveBeenNthCalledWith(1, '- a\n- b\n- c\n');
    expect(consoleLogSpy).toHaveBeenNthCalledWith(2, '');
    consoleLogSpy.mockRestore();
  });

  it(validateEnums.name, () => {
    expect(validateEnums('a', 'b', ['b'])).toBeUndefined();

    const f = (): void => {
      validateEnums('a', 'b', ['c', 'd']);
    };
    expect(f).toThrow(new Error('`a` must be one of ["c", "d"], but got "b"'));
  });
});
