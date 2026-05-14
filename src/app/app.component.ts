import { Component, signal } from '@angular/core';
import { HeaderComponent } from './header/header.component';
import { FileInputComponent } from './file.input/file.input.component';
import { AxisInputsComponent } from './axis.inputs/axis.inputs.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [HeaderComponent, FileInputComponent, AxisInputsComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
})
export class AppComponent {
  protected readonly title = signal('my-angular-app');
}
