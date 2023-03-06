import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class SearchService {

  constructor(private http: HttpClient) { }

  getVideos(value: any){
    return this.http.get('http://127.0.0.1:8000/getVideos/' + value);
  }
}
