export interface LogItem {
  id: number;
  label: string;
  key: any
}

export interface LogList {
  logs: Array<LogItem>;
}
