import { Component, OnInit, Input } from '@angular/core';
import { ReviewForm } from '../models/review-form.model';

@Component({
  selector: 'app-review-form',
  templateUrl: './review-form.component.html',
  styleUrls: ['./review-form.component.scss']
})
export class ReviewFormComponent implements OnInit {
  @Input() reviewForm!: ReviewForm;
  btnText! : string;

  ngOnInit() {
    this.btnText = 'Predict'
  }

  onAddReview() {
    if (this.btnText === 'Predict'){
      this.reviewForm.snaps++;
      this.btnText = 'DEJA COMMENTE ! ';
    } else {
      this.reviewForm.snaps--;
      this.btnText = 'Predict';

    }
  }


}
