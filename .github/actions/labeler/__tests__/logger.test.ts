import { Logger } from '../src/logger';

describe(Logger.name, (): void => {
  let logger: Logger;
  let consoleLogSpy: jest.SpyInstance<void, [any?, ...any[]]>;

  beforeAll((): void => {
    consoleLogSpy = jest.spyOn(console, 'log').mockImplementation();
  });

  afterEach((): void => {
    consoleLogSpy.mockReset();
  });

  afterAll((): void => {
    consoleLogSpy.mockRestore();
  });

  it('`log` should print a given message by default (quiet is false)', (): void => {
    logger = new Logger();

    logger.log('a');
    expect(consoleLogSpy).toHaveBeenCalledTimes(1);
    expect(consoleLogSpy).toHaveBeenLastCalledWith('a');
  });

  it('`log` should not print anything when quiet is true', (): void => {
    logger = new Logger(true);
    logger.log('a');
    expect(consoleLogSpy).not.toHaveBeenCalled();
  });
});
