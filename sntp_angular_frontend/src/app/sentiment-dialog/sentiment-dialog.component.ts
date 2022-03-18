import { Component, Inject } from '@angular/core';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { PredictionData } from '../../models/prediction-data';


@Component({
  selector: 'sentiment-dialog',
  templateUrl: './sentiment-dialog.component.html',
  styleUrls: ['./sentiment-dialog.component.scss']
})
export class SentimentDialog {
  constructor(
    public dialogRef: MatDialogRef<SentimentDialog>,
    @Inject(MAT_DIALOG_DATA) public data: PredictionData, ) {
      dialogRef.beforeClosed().subscribe(() => dialogRef.close(this.data));
  }

  onNoClick(): void {
    console.log(this.data);
    if(this.data.prediction === "positive") {
      this.data.prediction = "negative";
    } else {
      this.data.prediction = "positive";
    }
    this.dialogRef.close()
  }

  onYesClick(): void {
    this.dialogRef.close(this.data);
  }
}
