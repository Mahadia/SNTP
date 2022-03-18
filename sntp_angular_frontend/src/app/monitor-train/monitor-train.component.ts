import { Component, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';

import { MonitorTrainService } from './monitor-train.service';

import { TrainData, ImgFilePath } from '../../models/train-data';
import { LogList } from '../../models/log-data';



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

  imgPath: string = "";

  constructor(private monTrainService: MonitorTrainService) {
  }

  ngOnInit() {
    this.monTrainService.getDsData()
    .subscribe((data: TrainData) => {
      this.t_cnt = data.total;
      this.p_cnt = data.positive;
      this.n_cnt = data.negative;
      this.p_perc = (this.p_cnt / this.t_cnt) * 100;
      this.n_perc = (this.n_cnt / this.t_cnt) * 100;
    });
    this.monTrainService.getTrainFig()
    .subscribe((data: ImgFilePath) => {
      this.imgPath = data.img;
    });
  }

}
