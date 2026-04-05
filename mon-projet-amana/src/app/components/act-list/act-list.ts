/*import { Component } from '@angular/core';

@Component({
  selector: 'app-act-list',
  imports: [],
  templateUrl: './act-list.html',
  styleUrl: './act-list.css',
})
export class ActList {}*/
import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-act-list',
  templateUrl: './act-list.component.html'
})
export class ActListComponent implements OnInit {
  acts: any[] = [];
  apiUrl = 'http://localhost:8000/acts';

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.http.get<any[]>(this.apiUrl).subscribe(data => this.acts = data);
  }
}
