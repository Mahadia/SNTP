import { Component, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';

import { MonitorUsersService } from './monitor-users.service';
import { UsersData } from '../../models/users-data';

@Component({
  selector: 'app-monitor-users',
  templateUrl: './monitor-users.component.html',
  styleUrls: ['./monitor-users.component.scss']
})
export class MonitorUsersComponent {

  t_revs: number = 0;
  p_revs: number = 0;
  n_revs: number = 0;
  p_perc: number = 0;
  n_perc: number = 0;

  constructor(private monUsersService: MonitorUsersService) {
  }

  ngOnInit() {
    this.monUsersService.getUsersData()
    .subscribe( (data: UsersData) => {
      this.t_revs = data.total;
      this.p_revs = data.positive;
      this.n_revs = data.negative;
      this.p_perc = (this.p_revs / this.t_revs) * 100;
      this.n_perc = (this.n_revs / this.t_revs) * 100;
    });
  }

}
