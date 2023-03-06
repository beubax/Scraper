import { Component, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { SearchService } from '../search.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {


  constructor(private service: SearchService, private router: Router, private snackBar: MatSnackBar) { }

  ngOnInit(): void {
  }

  value: any; 
  input: any;
  videos: any;
  flag_button = false;
  flag_progress = false;

  //Method to submit search keyword
  searchSubmit(){
    if(this.value == this.input){
      console.log("You have already made a search.")
    }
    else{
      if(this.value != null){
        this.input = this.value;
        this.value = ' '
        this.flag_progress = true;
        this.service.getVideos(this.input).subscribe(res => {
          this.videos = res; //Storing json response from http request
          console.log(this.videos);
          this.flag_button = true;
          this.flag_progress = false;
          localStorage.setItem('paths', JSON.stringify(this.videos)); //Save json response in localstorage  
        },
        err => {console.log(err)})
      }   
    }
    
}

  //Redirects to videos page
  viewVideos(){
    this.router.navigate(['/videos/youtube']);
  }

}
