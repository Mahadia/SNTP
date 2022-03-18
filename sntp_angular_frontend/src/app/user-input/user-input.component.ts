import { Component, Inject } from '@angular/core';
import { FormBuilder } from '@angular/forms';

import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';

import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { SentimentDialog } from '../sentiment-dialog/sentiment-dialog.component';

import { PredictionData } from '../../models/prediction-data';
import { UserInputService } from './user-input.service';

@Component({
  selector: 'app-user-input',
  templateUrl: './user-input.component.html',
  styleUrls: ['./user-input.component.scss']
})
export class UserInputComponent {

  public textAreaValue: string = '';
  public predictData: PredictionData;

  private SERVER_URL: string = 'api/';
  public IMAGE_URL: string = 'https://source.unsplash.com/random/600x400'

  public resetter: boolean = false;

  constructor(private userInputService: UserInputService,
              private formBuilder: FormBuilder,
              public dialog: MatDialog) {
    this.predictData = {
      action: "",
      text: "",
      prediction: "",
      date: ""
    };
  }

  onSubmit(): void {
    // If we have text send it to backend for prediction
    if (this.textAreaValue) {
      this.predictData.text = this.textAreaValue;

      this.userInputService.postPrediction(this.predictData)
      .subscribe((data: PredictionData) => {
        this.predictData = {
          action: data.action,
          text: data.text,
          prediction: data.prediction,
          date: data.date,
      };
    this.openDialog();});
    }
  }

  openDialog(): void {
    const dialogRef = this.dialog.open(SentimentDialog, {
      width: '400px',
      disableClose: true,
      data: this.predictData,
    });

    dialogRef.afterClosed().subscribe(result => {
      this.textAreaValue = '';
      this.userInputService.postRecord( result )
      .subscribe((data) => {
        if(data.status === "failure") {
          alert("Failed to record prediction data.")
        } else {
          alert("Successfully recorded prediction data.")
        }
        window.location.reload();
      });
    });
  }

  onReset(): void {
    this.textAreaValue = "";
  }

}
