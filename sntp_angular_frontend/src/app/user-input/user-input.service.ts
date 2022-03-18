import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpErrorResponse, HttpResponse } from '@angular/common/http';

import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';

import { PredictionData } from '../../models/prediction-data';

export interface ReturnMessage {
  status: string;
}

@Injectable()
export class UserInputService {
  configUrl = 'http://127.0.0.1:5000';

  private SERVER_URL: string = 'api/';

  constructor(private http: HttpClient) { }

  postPrediction(data: PredictionData) {
    data.action = 'predict';
    return this.http.post<PredictionData>(this.SERVER_URL, data).pipe(
      catchError(this.handleError));
  }

  postRecord(data: PredictionData) {
    return this.http.post<ReturnMessage>(this.SERVER_URL, data).pipe(
      catchError(this.handleError));
  }


    //return this.http.get<any>(this.SERVER_URL, {params: {target: "monitor_data"}})
         // .pipe(
       // catchError(this.handleError)
      //);
      //}

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
