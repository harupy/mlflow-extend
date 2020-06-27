export class Logger {
  constructor(private quiet: boolean = false) {}

  log(message?: any, ...optionalParams: any[]): void {
    if (!this.quiet) {
      console.log(message, ...optionalParams);
    }
  }
}
