import { LoggingLevel, Logger } from '../src/logger';

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

  test('LoggingLevel: DEBUG', (): void => {
    logger = new Logger(LoggingLevel.DEBUG);
    logger.debug('a');
    logger.info('b');

    expect(consoleLogSpy).toHaveBeenCalledTimes(2);
    expect(consoleLogSpy).toHaveBeenNthCalledWith(1, 'a');
    expect(consoleLogSpy).toHaveBeenNthCalledWith(2, 'b');
  });

  it('LoggingLevel: INFO', (): void => {
    logger = new Logger(LoggingLevel.INFO);
    logger.debug('a');
    logger.info('b');

    expect(consoleLogSpy).toHaveBeenCalledTimes(1);
    expect(consoleLogSpy).toHaveBeenNthCalledWith(1, 'b');
  });

  it('setLevel', (): void => {
    logger = new Logger(LoggingLevel.INFO);
    logger.debug('a');
    logger.setLevel(LoggingLevel.DEBUG);
    logger.debug('b');

    expect(consoleLogSpy).toHaveBeenCalledTimes(1);
    expect(consoleLogSpy).toHaveBeenCalledWith('b');
  });
});
