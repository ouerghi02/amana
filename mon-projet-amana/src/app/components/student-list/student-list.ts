/*import { Component } from '@angular/core';

@Component({
  selector: 'app-student-list',
  imports: [],
  templateUrl: './student-list.html',
  styleUrl: './student-list.css',
})
export class StudentList {}*/
import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-student-list',
  templateUrl: './student-list.component.html',
  styleUrls: ['./student-list.component.css']
})
export class StudentListComponent implements OnInit {
  students: any[] = [];
  apiUrl = 'http://localhost:8000/students';

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.getStudents();
  }

  getStudents() {
    this.http.get<any[]>(this.apiUrl).subscribe(data => this.students = data);
  }

  deleteStudent(id: number) {
    this.http.delete(`${this.apiUrl}/${id}`).subscribe(() => this.getStudents());
  }
}
