import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import {
  HttpClientModule,
  HTTP_INTERCEPTORS,
  HttpClientXsrfModule,
} from '@angular/common/http';
import { APP_BASE_HREF } from '@angular/common';

import { AppComponent } from './app.component';
import { UserDisplayComponent } from './components/user-display/user-display.component';
import { AppRoutingModule } from './app-routing.module';
import { AuthInterceptor } from './interceptors/auth.interceptor';
import { SubmitDisplayComponent } from './components/submit-display/submit-display.component';
import { ReviewDisplayComponent } from './components/review-display/review-display.component';
import { CookieService } from 'ngx-cookie-service';
import { LoggerComponent } from './components/logger-display/logger.component';
import { EditDisplayComponent } from './components/edit-display/edit-display.component';

@NgModule({
  declarations: [
    AppComponent,
    UserDisplayComponent,
    SubmitDisplayComponent,
    ReviewDisplayComponent,
    LoggerComponent,
    EditDisplayComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    HttpClientXsrfModule.withOptions({
      cookieName: 'csrftoken',
      headerName: 'X-CSRFToken',
    }),
    AppRoutingModule,
  ],
  providers: [
    CookieService,
    [{ provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true }],
    [{ provide: APP_BASE_HREF, useValue: '/' }],
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
