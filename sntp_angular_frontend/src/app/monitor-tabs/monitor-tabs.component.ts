import { Component, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-monitor-tabs',
  templateUrl: './monitor-tabs.component.html',
  styleUrls: ['./monitor-tabs.component.scss']
})
export class MonitorTabsComponent {

  public imgPath: string = '/assets/img/user_phold.png';

  @Output() tabEvent = new EventEmitter<string>();

  constructor() {
  }

  onUsersData() {
    this.tabEvent.emit("users_data");
  }

  onTrainData() {
    this.tabEvent.emit("train_data");
  }
}
