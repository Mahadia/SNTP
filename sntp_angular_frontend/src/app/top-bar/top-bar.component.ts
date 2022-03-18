import { Component, Output, EventEmitter } from '@angular/core';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { LoginDialog } from '../login-dialog/login-dialog.component';


@Component({
  selector: 'app-top-bar',
  templateUrl: './top-bar.component.html',
  styleUrls: ['./top-bar.component.scss']
})
export class TopBarComponent {

  public login_state: boolean = false;

  private u_name: string = "admin";
	private p_word: string = "password123";

  public btnLabel: string = "Login";

  public imgPath: string = "/assets/img/logo2.png";

  @Output() loginEvent = new EventEmitter<boolean>();

  constructor(public dialog: MatDialog) {
  }

  loginHandler(): void {
    if(this.login_state){
      this.login_state = false;
      this.btnLabel = "Login";
      this.loginEvent.emit(false);
    } else {
      this.openDialog();
    }
  }

  openDialog(): void {
    const dialogRef = this.dialog.open(LoginDialog, {
      width: '400px',
      disableClose: true
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log('The login dialog was closed');
      if(result.event === 'login') {
        if(result.data.username === this.u_name && result.data.password === this.p_word){
          this.login_state = true;
          this.btnLabel = "Logout";
          this.loginEvent.emit(true);
        } else {
          this.login_state = false;
          this.loginEvent.emit(false);
          alert("Access denied !");
        }
      }
    });
  }

}
