import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { InstagramComponent } from './instagram/instagram.component';
import { TiktokComponent } from './tiktok/tiktok.component';
import { VideosComponent } from './videos/videos.component';
import { YoutubeComponent } from './youtube/youtube.component';

const routes: Routes = [
  {path: '', component: HomeComponent},
  {path:'home', component: HomeComponent},
  {
    path: 'videos', component: VideosComponent,
    children: [
      { path: 'youtube', component: YoutubeComponent },
      { path: 'tiktok', component: TiktokComponent },
      { path: 'instagram', component: InstagramComponent }
    ]
  },

  
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
