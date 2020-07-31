import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms'; 
import { HttpClientModule, HTTP_INTERCEPTORS, HttpClientXsrfModule } from '@angular/common/http';

import { AppComponent } from './app.component';
import { UserDisplayComponent } from './components/user-display/user-display.component';
import { AppRoutingModule } from './app-routing.module';
import { AuthInterceptor } from './interceptors/auth.interceptor';
import { SubmitDisplayComponent } from './components/submit-display/submit-display.component';
import { ReviewDisplayComponent } from './components/review-display/review-display.component';
import { CookieService } from 'ngx-cookie-service';
import { LoggerComponent } from './components/logger/logger.component';

@NgModule({
  declarations: [
    AppComponent,
    UserDisplayComponent,
    SubmitDisplayComponent,
    ReviewDisplayComponent,
    LoggerComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpClientModule,
    HttpClientXsrfModule.withOptions({
      cookieName: 'csrftoken',
      headerName: 'X-CSRFToken'
    }),
    AppRoutingModule
  ],
  providers: [     
    CookieService,       
    [ { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true } ],
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
