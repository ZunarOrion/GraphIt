import { Component, signal } from '@angular/core';
import { HeaderComponent } from './header/header.component';
import { InputsComponent } from './inputs/inputs.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [HeaderComponent, InputsComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
})
export class AppComponent {
  protected readonly title = signal('my-angular-app');
}
