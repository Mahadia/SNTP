import { Component, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';

import { MonitorTrainService } from './monitor-train.service';

import { TrainData, TrainGraph } from '../../models/train-data';
import { LogList, LogItem } from '../../models/log-data';

import {DomSanitizer, SafeResourceUrl, SafeUrl} from '@angular/platform-browser';


@Component({
  selector: 'app-monitor-train',
  templateUrl: './monitor-train.component.html',
  styleUrls: ['./monitor-train.component.scss']
})
export class MonitorTrainComponent {

  t_cnt: number = 0;
  p_cnt: number = 0;
  n_cnt: number = 0;
  p_perc: number = 0;
  n_perc: number = 0;

  logCount: number = 0;
  logList: LogList = {logs: []};

  public myGraph : any;
  private readonly imageType : string = 'data:image/PNG;base64,';

  constructor(private monTrainService: MonitorTrainService,
              private mySanitizer: DomSanitizer) {
  }

  ngOnInit() {
    this.monTrainService.getDsData()
    .subscribe((data: TrainData) => {
      this.t_cnt = data.total;
      this.p_cnt = data.positive;
      this.n_cnt = data.negative;
      this.p_perc = Math.round((this.p_cnt / this.t_cnt) * 100);
      this.n_perc = Math.round((this.n_cnt / this.t_cnt) * 100);
    });
    this.monTrainService.getLogData()
    .subscribe((data: LogList) => {
      console.log(data);
      this.logList = data;
      this.logCount = data.logs.length;
      console.log(this.logCount);
    });
    this.monTrainService.getGraph()
    .subscribe((data: TrainGraph ) => {
      this.myGraph = this.mySanitizer.bypassSecurityTrustUrl(this.imageType + data.image);
    });
  }

}
