import { Component, Inject } from '@angular/core';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';

export interface LoginData {
  username: string;
  password: string;
}

@Component({
  selector: 'login-dialog',
  templateUrl: './login-dialog.component.html',
  styleUrls: ['./login-dialog.component.scss']
})
export class LoginDialog {

  login_data: any;

  constructor(
    public dialogRef: MatDialogRef<LoginDialog>,
    @Inject(MAT_DIALOG_DATA) public data: LoginData, ) {
      this.login_data = {username: "", password: ""}
  }

  onLoginClick(): void {
    this.dialogRef.close({event: 'login', data: this.login_data});
  }

  onCancelClick(): void {
    this.dialogRef.close();
  }
}
