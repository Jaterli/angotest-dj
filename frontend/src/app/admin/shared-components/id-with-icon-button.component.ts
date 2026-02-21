import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-id-with-icon-button',
  standalone: true, 
  template: `
    <div class="flex items-center gap-1 text-xs text-gray-500 dark:text-gray-400 mt-0.5">
      @if (showId && itemId) {
        <span>#{{ itemId }}</span>
      }
      <button (click)="onStatsClick()"
              class="inline-flex items-center justify-center p-0.5 text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 transition-colors"
              title="Ver estadísticas detalladas">
        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd"/>
        </svg>
      </button>
    </div>
  `
})
export class IdWithIconButtonComponent {
  @Input() itemId?: number;
  @Input() showId: boolean = true; // Valor por defecto: true (se muestra el ID)
  @Output() statsClick = new EventEmitter<number>();

  onStatsClick() {
     this.statsClick.emit(this.itemId);
  }
}