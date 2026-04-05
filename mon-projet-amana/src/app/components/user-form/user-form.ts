/*import { Component } from '@angular/core';

@Component({
  selector: 'app-user-form',
  imports: [],
  templateUrl: './user-form.html',
  styleUrl: './user-form.css',
})
export class UserForm {}*/
import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-user-form',
  templateUrl: './user-form.component.html'
})
export class UserFormComponent {
  user = { full_name: '', email: '', password_hash: '', role: 'user' };
  apiUrl = 'http://localhost:8000/users';

  constructor(private http: HttpClient) {}

  onSubmit() {
    this.http.post(this.apiUrl, this.user).subscribe({
      next: () => alert("Utilisateur créé avec succès !"),
      error: () => alert("Erreur lors de la création")
    });
  }
}
