import { sample } from '../src/main';

describe('main', (): void => {
  it('sample', (): void => {
    expect(sample()).toEqual('sample');
  });
});
