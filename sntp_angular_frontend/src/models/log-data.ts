export interface AccLoss {
  accuracy: number;
  loss: number;
}

export interface LogItem {
  timestamp: string;
  winner: string;
  new_model: AccLoss;
  old_model: AccLoss;
}

export interface LogList {
  logs: Array<LogItem>;
}
