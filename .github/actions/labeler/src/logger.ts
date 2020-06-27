export enum LoggingLevel {
  DEBUG,
  SILENT,
}

export class Logger {
  constructor(private level: LoggingLevel = 0) {}

  private log(message?: any, ...optionalParams: any[]): void {
    console.log(message, ...optionalParams);
  }

  private shouldLog(level: LoggingLevel): boolean {
    return this.level <= level;
  }

  debug(message?: any, ...optionalParams: any[]): void {
    if (this.shouldLog(LoggingLevel.DEBUG)) {
      this.log(message, ...optionalParams);
    }
  }

  setLevel(newLevel: LoggingLevel) {
    this.level = newLevel;
  }
}
