import { Component, OnInit } from '@angular/core';
import { ReviewForm } from './models/review-form.model';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  myReview!: ReviewForm;
  myOtherReview! : ReviewForm;
  myLastReview! : ReviewForm;

  ngOnInit() {
    this.myReview = new ReviewForm('Add Review','Please write you review for prediction',
    new Date(), 6,
    'https://img.freepik.com/photos-gratuite/prise-vue-au-grand-angle-seul-arbre-poussant-sous-ciel-assombri-pendant-coucher-soleil-entoure-herbe_181624-22807.jpg'
    );
    this.myOtherReview = new ReviewForm('Add ReALiview','Please write AAAA',
    new Date(), 100,
    'https://images.bfmtv.com/52fhxutEmVO4ty9jQb0qn7cPEpc=/0x0:1280x720/860x0/images/Resume-Real-Madrid-Q-3-1-Paris-SG-Ligue-des-champions-8e-de-finale-retour-1366632.jpg'
    );

  }
}

