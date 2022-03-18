import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouterModule } from '@angular/router';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatDialogModule } from '@angular/material/dialog';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { HttpClientModule } from '@angular/common/http';
import { HttpClientXsrfModule } from '@angular/common/http';

import { AppComponent } from './app.component';
import { TopBarComponent} from './top-bar/top-bar.component';
import { AppViewComponent } from './app-view/app-view.component';

import { UserInputComponent } from './user-input/user-input.component';
import { UserInputService } from './user-input/user-input.service';
import { SplashComponent } from './splash/splash.component'

import { MonitorTabsComponent } from './monitor-tabs/monitor-tabs.component';
import { MonitorUsersComponent } from './monitor-users/monitor-users.component';
import { MonitorUsersService } from './monitor-users/monitor-users.service';
import { MonitorTrainComponent } from './monitor-train/monitor-train.component';
import { MonitorTrainService } from './monitor-train/monitor-train.service';

import { SentimentDialog } from './sentiment-dialog/sentiment-dialog.component';
import { LoginDialog } from './login-dialog/login-dialog.component';


@NgModule({
  declarations: [
    AppComponent,
    TopBarComponent,
    AppViewComponent,
    UserInputComponent,
    SplashComponent,
    MonitorTabsComponent,
    MonitorUsersComponent,
    MonitorTrainComponent,
    SentimentDialog,
    LoginDialog,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    MatDialogModule,
    BrowserAnimationsModule,
    RouterModule.forRoot([
    	{ path: 'app-view-component', component: AppViewComponent },
    	{ path: '',   redirectTo: '/app-view-component', pathMatch: 'full' },
    ]),
    HttpClientModule,
    HttpClientXsrfModule.withOptions({
      cookieName: 'My-Xsrf-Cookie',
      headerName: 'My-Xsrf-Header',
    }),
  ],
  providers: [
    UserInputService,
    MonitorUsersService,
    MonitorTrainService,
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
