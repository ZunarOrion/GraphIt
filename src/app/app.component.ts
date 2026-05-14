import { Component, signal } from '@angular/core';
import { HeaderComponent } from './header/header.component';
import { FileInputComponent } from './file.input/file.input.component';
import { AxisInputsComponent } from './axis.inputs/axis.inputs.component';
import { DisplayBoxComponent } from './display.box/display.box.component';
import { RenderButtonComponent } from './render.button/render.button.component';
import { FooterComponent } from './footer/footer.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    HeaderComponent,
    FileInputComponent,
    AxisInputsComponent,
    DisplayBoxComponent,
    RenderButtonComponent,
    FooterComponent,
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
})
export class AppComponent {
  protected readonly title = signal('my-angular-app');
}
