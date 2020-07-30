import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms'; 
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';

import { AppComponent } from './app.component';
import { UserDisplayComponent } from './components/user-display/user-display.component';
import { AppRoutingModule } from './app-routing.module';
import { AuthInterceptor } from './interceptors/auth.interceptor';
import { SubmitDisplayComponent } from './components/submit-display/submit-display.component';

@NgModule({
  declarations: [
    AppComponent,
    UserDisplayComponent,
    SubmitDisplayComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpClientModule,
    AppRoutingModule
  ],
  providers: [            
    [ { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true } ],
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
