import { Component, OnInit, ViewChild } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-youtube',
  templateUrl: './youtube.component.html',
  styleUrls: ['./youtube.component.css']
})
export class YoutubeComponent implements OnInit {

  data: any; //Variable to hold json response from http request

  constructor(private router:Router) {}

  ngOnInit(): void {
    this.data = JSON.parse(localStorage.getItem('paths') || '{}'); //On page initialization, store json response from localstorage 
  }

  //Video player methods to play/pause video
  @ViewChild('videoplayer') private videoplayer: any;
  toggleVideo(event: any) {
    this.videoplayer.nativeElement.play();
    this.videoplayer.nativeElement.pause();

}
}
