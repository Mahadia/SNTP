import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpErrorResponse, HttpResponse } from '@angular/common/http';

import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';

import { TrainData, ImgFilePath } from '../../models/train-data';
import { LogList } from '../../models/log-data';


@Injectable()
export class MonitorTrainService {
  configUrl = 'http://127.0.0.1:5000';

  private SERVER_URL: string = 'api/';

  constructor(private http: HttpClient) { }

  getDsData() {
    return this.http.get<TrainData>(this.SERVER_URL,{ params: {target: "dataset_data" }}).pipe(catchError(this.handleError));
    }

  getLogData() {
    return this.http.get<LogList>(this.SERVER_URL,{ params: {target: "log_data" }})
            .pipe(catchError(this.handleError));
    }

    getTrainFig(){
      return this.http.get<ImgFilePath>(this.SERVER_URL,{ params: {target: "train_graph" }})
              .pipe(catchError(this.handleError));
      }


  private handleError(error: HttpErrorResponse) {
    alert("We apologize there has been an error,\nplease try again later.");
    if (error.status === 0) {
      // A client-side or network error occurred. Handle it accordingly.
      console.error('An error occurred:', error.error);
    } else {
      // The backend returned an unsuccessful response code.
      // The response body may contain clues as to what went wrong.
      console.error(
        `Backend returned code ${error.status}, body was: `, error.error);
    }
    // Return an observable with a user-facing error message.
    return throwError(() => new Error('Something bad happened; please try again later.'));
  }

}
