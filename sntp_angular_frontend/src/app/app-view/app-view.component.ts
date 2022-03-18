import { Component, Inject } from '@angular/core';

import { TopBarComponent } from '../top-bar/top-bar.component';

import { UserInputComponent } from '../user-input/user-input.component';
import { SplashComponent } from '../splash/splash.component';
import { MonitorTabsComponent } from '../monitor-tabs/monitor-tabs.component';
import { MonitorUsersComponent } from '../monitor-users/monitor-users.component';
import { MonitorTrainComponent } from '../monitor-train/monitor-train.component';


@Component({
  selector: 'app-view',
  templateUrl: './app-view.component.html',
  styleUrls: ['./app-view.component.scss']
})
export class AppViewComponent {

  public adminUser: boolean = false;

  public dataType: string = "users_data";

  constructor() {
  }

  loginRequest(state: boolean) {
    console.log("Login event.");
    console.log(state);
    this.adminUser = state;
  }

  dataRequest(data: string) {
    this.dataType = data;
  }

}
