import { extractLabels, getName } from '../src/main';

describe('main', (): void => {
  it('extractLabels', (): void => {
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

  it('getName', (): void => {
    expect(getName({name: 'a'})).toEqual('a')
  })
});
