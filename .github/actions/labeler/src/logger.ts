export enum LoggingLevel {
  DEBUG = 0,
  INFO = 1,
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

  info(message?: any, ...optionalParams: any[]): void {
    if (this.shouldLog(LoggingLevel.INFO)) {
      this.log(message, ...optionalParams);
    }
  }

  setLevel(newLevel: LoggingLevel) {
    this.level = newLevel;
  }
}
