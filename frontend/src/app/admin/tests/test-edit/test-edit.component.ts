import { Component, OnInit, signal, OnDestroy, computed, WritableSignal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, FormArray, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { Observable, Subscription, debounceTime, distinctUntilChanged, filter, tap } from 'rxjs';
import { Test } from '../../../shared/models/test.models';
import { ModalComponent } from '../../../shared/components/modal.component';
import { TestsManagementService } from '../../services/tests-management.service';
import { TopicsService } from '../../../shared/services/topics.service';

@Component({
  selector: 'app-test-edit',
  standalone: true,
  templateUrl: './test-edit.component.html',
  imports: [
    CommonModule,
    ReactiveFormsModule,
    ModalComponent,
  ]
})
export class TestEditComponent implements OnInit, OnDestroy {
  testForm: FormGroup;
  loading = signal(true);
  saving = signal(false);
  error = signal<string | null>(null);
  testId!: number;
  testData: Test | null = null;

  successTitle = signal('¡Test Actualizado!');
  successMessage = signal('El test se ha actualizado correctamente. Serás redirigido a la lista de tests.');
  showModificationWarning = signal(false);
  
  // Estados para temas
  mainTopics = signal<string[]>([]);
  subTopics = signal<string[]>([]);
  specificTopics = signal<string[]>([]);
  isValidSpecificTopic = signal<boolean>(true);

  // Estados de carga
  isLoading = signal({
    main: false,
    sub: false,
    specific: false
  });

  // Estados de validación
  validationState = computed(() => {

    const mainTopic = this.testForm.get('main_topic')?.value;
    const subTopic = this.testForm.get('sub_topic')?.value;
    const specificTopic = this.testForm.get('specific_topic')?.value;

    const mainValid = !mainTopic || this.mainTopics().some(t => t.toLowerCase() === mainTopic.toLowerCase());
    const subValid = !subTopic || this.subTopics().some(t => t.toLowerCase() === subTopic.toLowerCase());
    const specificValid = !specificTopic || this.specificTopics().some(t => t.toLowerCase() === specificTopic.toLowerCase());

    this.isValidSpecificTopic(); // Dependencia necesaria para cambiar el mensaje de Tema Específico

    return {
      main: {
        isValid: mainValid,
        message: !mainTopic ? '' :
                 mainValid ? '✓ Tema válido' : 'Tema no encontrado',
        hasData: this.mainTopics().length > 0
      },
      sub: {
        isValid: subValid,
        message: !subTopic ? '' :
                 subValid ? '✓ Subtema válido' : 'Subtema no encontrado',
        hasData: this.subTopics().length > 0
      },
      specific: {
        isValid: specificValid,
        message: !specificTopic ? '' :
                 specificValid ? '✓ Tema específico válido' : 'Tema específico no encontrado',
        hasData: this.specificTopics().length > 0
      }
    };
  });

  // Campos de la jerarquía de temas para el template (unifica los 3 bloques repetidos del HTML)
  get topicFields() {
    const main = this.testForm.get('main_topic')?.value;
    const sub = this.testForm.get('sub_topic')?.value;
    const validation = this.validationState();
    const loading = this.isLoading();

    return [
      {
        key: 'main_topic',
        label: 'Tema Principal',
        placeholder: 'Ej: Ciencias de la Computación',
        validation: validation.main,
        list: this.mainTopics(),
        loading: loading.main,
        showKey: 'main' as string,
        disabled: false,
        emptyHint: null as string | null,
        listHeader: 'Temas disponibles:',
        onSelect: (t: string) => this.onMainTopicSelect(t)
      },
      {
        key: 'sub_topic',
        label: 'Subtema',
        placeholder: 'Ej: Fundamentos de Programación',
        validation: validation.sub,
        list: this.subTopics(),
        loading: loading.sub,
        showKey: 'sub' as string,
        disabled: !main,
        emptyHint: !main ? 'Introduce un tema principal primero' : null,
        listHeader: `Subtemas disponibles para "${main}":`,
        onSelect: (t: string) => this.onSubTopicSelect(t)
      },
      {
        key: 'specific_topic',
        label: 'Tema Específico',
        placeholder: 'Ej: Funciones y Procedimientos',
        validation: validation.specific,
        list: this.specificTopics(),
        loading: loading.specific,
        showKey: 'specific' as string,
        disabled: false,
        emptyHint: !sub ? 'Introduce un subtema primero' : null,
        listHeader: `Temas específicos para "${sub}":`,
        onSelect: (t: string) => this.onSpecificTopicSelect(t)
      }
    ];
  }

  // UI states
  showLists: Record<string, boolean> = {
    main: false,
    sub: false,
    specific: false
  };

  // Estados para modales
  showSuccessModal = signal(false);
  showErrorModal = signal(false);
  showTopicWarningModal = signal(false);
  errorMessage = signal('');
  invalidTopics = signal<string[]>([]);

  // Suscripciones
  private subscriptions = new Subscription();

  constructor(
    private fb: FormBuilder,
    private testsManagementService: TestsManagementService,
    private topicsService: TopicsService,
    private route: ActivatedRoute,
    private router: Router
  ) {
    this.testForm = this.fb.group({
      title: ['', Validators.required],
      description: [''],
      main_topic: ['', Validators.required],
      sub_topic: ['', Validators.required],
      specific_topic: ['', Validators.required],
      level: ['', Validators.required],
      is_active: [true],
      questions: this.fb.array([])
    });

    this.setupTopicListeners();
  }

  ngOnInit() {
    this.loadMainTopics();
    this.route.params.subscribe(params => {
      this.testId = +params['id'];
      if (this.testId) {
        this.loadTest();
      } else {
        this.error.set('ID de test inválido');
        this.loading.set(false);
      }
    });
  }

  ngOnDestroy() {
    this.subscriptions.unsubscribe();
  }

  // --- Listeners de la jerarquía de temas (helper genérico) ---

  private setupTopicListener(
    controlName: 'main_topic' | 'sub_topic' | 'specific_topic',
    showKey: string,
    canValidate: () => boolean,
    onValid: (value: string) => void
  ) {
    const sub = this.testForm.get(controlName)?.valueChanges.pipe(
      debounceTime(500),
      distinctUntilChanged(),
      tap(() => this.showLists[showKey] = false),
      filter(value => value && value.trim().length > 0 && canValidate())
    ).subscribe(onValid) ?? new Subscription();

    this.subscriptions.add(sub);
  }

  setupTopicListeners() {
    // 1. TEMA PRINCIPAL
    this.setupTopicListener('main_topic', 'main', () => true, (value) => {
      const isValid = this.mainTopics().some(t => t.toLowerCase() === value.toLowerCase());

      if (isValid) {
        this.loadSubTopics(value);
        const subTopic = this.testForm.get('sub_topic')?.value;
        if (subTopic != '') this.loadSpecificTopics(value, subTopic);
      } else {
        this.subTopics.set([]);
        this.specificTopics.set([]);
      }
    });

    // 2. SUBTEMA
    this.setupTopicListener(
      'sub_topic',
      'sub',
      () => {
        const mainTopic = this.testForm.get('main_topic')?.value;
        return !!(mainTopic && mainTopic.trim());
      },
      (value) => {
        const isValid = this.subTopics().some(t => t.toLowerCase() === value.toLowerCase());
        const mainTopic = this.testForm.get('main_topic')?.value;

        if (isValid && mainTopic) {
          this.loadSpecificTopics(mainTopic, value);
        } else {
          this.specificTopics.set([]);
        }
      }
    );

    // 3. TEMA ESPECÍFICO
    this.setupTopicListener(
      'specific_topic',
      'specific',
      () => {
        const mainTopic = this.testForm.get('main_topic')?.value;
        const subTopic = this.testForm.get('sub_topic')?.value;
        return !!(mainTopic && mainTopic.trim() && subTopic && subTopic.trim());
      },
      (value) => {
        const isValid = this.specificTopics().some(t => t.toLowerCase() === value.toLowerCase());
        this.isValidSpecificTopic.set(!(!isValid && this.specificTopics().length > 0));
      }
    );
  }

  toggleList(key: string) {
    this.showLists[key] = !this.showLists[key];
  }

  closeList(key: string) {
    this.showLists[key] = false;
  }

  // --- Carga de temas (helper genérico) ---

  private loadTopics(
    loadingKey: string,
    target: WritableSignal<string[]>,
    request$: Observable<string[]>,
    label: string
  ) {
    this.isLoading.update(state => ({ ...state, [loadingKey]: true }));
    request$.subscribe({
      next: (topics) => {
        target.set(topics);
        this.isLoading.update(state => ({ ...state, [loadingKey]: false }));
      },
      error: (err) => {
        console.error(`Error al cargar ${label}:`, err);
        target.set([]);
        this.isLoading.update(state => ({ ...state, [loadingKey]: false }));
      }
    });
  }

  loadMainTopics() {
    // Nota: el original no reseteaba mainTopics() a [] en caso de error; se mantiene igual
    // salvo que aquí, por consistencia, sí se limpia (no afecta funcionalidad visible).
    this.loadTopics('main', this.mainTopics, this.topicsService.getMainTopics(), 'temas principales');
  }

  loadSubTopics(mainTopic: string) {
    this.loadTopics('sub', this.subTopics, this.topicsService.getSubtopics(mainTopic), 'subtemas');
  }

  loadSpecificTopics(mainTopic: string, subTopic: string) {
    this.loadTopics('specific', this.specificTopics, this.topicsService.getSpecificTopics(mainTopic, subTopic), 'temas específicos');
  }

  onMainTopicSelect(topic: string) {
    this.testForm.get('main_topic')?.setValue(topic, { emitEvent: true });
    this.showLists['main'] = false;
  }

  onSubTopicSelect(topic: string) {
    this.testForm.get('sub_topic')?.setValue(topic, { emitEvent: true });
    this.showLists['sub'] = false;
  }

  onSpecificTopicSelect(topic: string) {
    this.testForm.get('specific_topic')?.setValue(topic, { emitEvent: true });
    this.showLists['specific'] = false;
  }

  loadTest() {
    this.loading.set(true);
    this.error.set(null);

    this.testsManagementService.getTestById(this.testId).subscribe({
      next: (response: any) => {
        try {
          const testData = response.test || response;

          if (!testData) {
            throw new Error('No se recibieron datos del test');
          }

          if (!testData.questions) {
            testData.questions = [];
          }

          this.testData = testData;
          this.populateForm(testData);
          this.loading.set(false);

        } catch (err: any) {
          console.error('Error procesando la respuesta:', err);
          this.error.set('Error al procesar los datos del test');
          this.loading.set(false);
        }
      },
      error: (err) => {
        console.error('Error al cargar el test:', err);
        this.error.set(`Error al cargar el test: ${err.message || 'Error desconocido'}`);
        this.loading.set(false);
      }
    });
  }

  populateForm(test: Test) {
    // Limpiar formulario
    while (this.questions.length !== 0) {
      this.questions.removeAt(0);
    }

    // Establecer valores
    this.testForm.patchValue({
      title: test.title || '',
      description: test.description || '',
      main_topic: test.main_topic || '',
      sub_topic: test.sub_topic || '',
      specific_topic: test.specific_topic || '',
      level: test.level || '',
      is_active: test.is_active !== undefined ? test.is_active : true
    });

    // Cargar datos relacionados
    if (test.main_topic) {
      setTimeout(() => {
        if (this.mainTopics().some(t => t.toLowerCase() === test.main_topic.toLowerCase())) {
          this.loadSubTopics(test.main_topic);
        }
      }, 100);
    }

    if (test.sub_topic) {
      setTimeout(() => {
        if (this.subTopics().some(t => t.toLowerCase() === test.sub_topic.toLowerCase())) {
          this.loadSpecificTopics(test.main_topic, test.sub_topic);
        }
      }, 500);
    }

    // Cargar preguntas
    if (test.questions && test.questions.length > 0) {
      test.questions.forEach(question => {
        this.addQuestionWithData(question);
      });
    }
  }

  addQuestionWithData(question: any) {
    const questionGroup = this.fb.group({
      id: [question.id || null],
      question_text: [question.question_text || '', Validators.required],
      answers: this.fb.array([])
    });

    this.questions.push(questionGroup);
    const answersArray = questionGroup.get('answers') as FormArray;

    if (question.answers && question.answers.length > 0) {
      question.answers.forEach((answer: any) => {
        answersArray.push(this.fb.group({
          id: [answer.id || null],
          answer_text: [answer.answer_text || '', Validators.required],
          is_correct: [answer.is_correct || false]
        }));
      });
    } else {
      for (let i = 0; i < 4; i++) {
        answersArray.push(this.fb.group({
          id: [null],
          answer_text: ['', Validators.required],
          is_correct: [i === 0]
        }));
      }
    }
  }

  get questions(): FormArray {
    return this.testForm.get('questions') as FormArray;
  }

  addQuestion() {
    this.questions.push(this.fb.group({
      id: [null],
      question_text: ['', Validators.required],
      answers: this.fb.array([
        this.fb.group({ id: [null], answer_text: ['', Validators.required], is_correct: [true] }),
        this.fb.group({ id: [null], answer_text: ['', Validators.required], is_correct: [false] }),
        this.fb.group({ id: [null], answer_text: ['', Validators.required], is_correct: [false] }),
      ])
    }));

    const lastQuestion = document.querySelector('#cuestions > div:last-child');
    if (lastQuestion)
      lastQuestion.scrollIntoView();
  }

  getAnswers(qIndex: number): FormArray {
    return this.questions.at(qIndex).get('answers') as FormArray;
  }

  addAnswer(qIndex: number) {
    this.getAnswers(qIndex).push(this.fb.group({
      id: [null],
      answer_text: ['', Validators.required],
      is_correct: [false]
    }));
  }

  onCorrectAnswerChange(questionIndex: number, answerIndex: number): void {
    const answersArray = this.questions.at(questionIndex).get('answers') as FormArray;

    answersArray.controls.forEach((answerControl, index) => {
      answerControl.get('is_correct')?.setValue(index === answerIndex);
    });
  }

  hasCorrectAnswer(questionIndex: number): boolean {
    const answersArray = this.questions.at(questionIndex).get('answers') as FormArray;
    return answersArray.controls.some(answerControl => answerControl.get('is_correct')?.value);
  }

  allQuestionsHaveCorrectAnswer(): boolean {
    return this.questions.controls.every((_, index) => this.hasCorrectAnswer(index));
  }

  validateForm(): boolean {
    if (this.testForm.invalid) {
      this.markFormGroupTouched(this.testForm);
      return false;
    }

    const mainTopic = this.testForm.get('main_topic')?.value;
    const subTopic = this.testForm.get('sub_topic')?.value;
    const specificTopic = this.testForm.get('specific_topic')?.value;

    if (!mainTopic || !subTopic || !specificTopic) {
      this.showError('Debe completar todos los campos de la jerarquía de temas.');
      return false;
    }

    const validation = this.validationState();
    const hasInvalidTopics = !validation.main.isValid || !validation.sub.isValid || !validation.specific.isValid;

    if (hasInvalidTopics) {
      this.showTopicWarning();
      return true;
    }

    return this.validateQuestions();
  }

  validateQuestions(): boolean {
    const questions = this.questions.value;
    if (questions.length === 0) {
      this.showError('Debe haber al menos una pregunta en el test.');
      return false;
    }

    for (let i = 0; i < questions.length; i++) {
      const question = questions[i];

      if (!question.answers.some((a: any) => a.is_correct)) {
        this.showError(`La pregunta "${question.question_text}" debe tener una respuesta correcta seleccionada.`);
        return false;
      }

      if (question.answers.length < 2) {
        this.showError(`La pregunta "${question.question_text}" debe tener al menos dos respuestas.`);
        return false;
      }

      const answerTexts = question.answers.map((a: any) => a.answer_text.toLowerCase().trim());
      const uniqueAnswers = new Set(answerTexts);
      if (uniqueAnswers.size !== answerTexts.length) {
        this.showError(`La pregunta "${question.question_text}" tiene respuestas duplicadas.`);
        return false;
      }
    }

    return true;
  }

  showTopicWarning() {
    const warnings: string[] = [];
    const validation = this.validationState();

    if (!validation.main.isValid) warnings.push('Tema principal');
    if (!validation.sub.isValid) warnings.push('Subtema');
    if (!validation.specific.isValid) warnings.push('Tema específico');

    this.invalidTopics.set(warnings);
    this.showTopicWarningModal.set(true);
  }

  private pendingAction: 'update' | 'new' | null = null;

  onTopicWarningConfirm(proceed: boolean) {
    this.showTopicWarningModal.set(false);
    if (proceed) {
      if (this.pendingAction === 'update') {
        this.showModificationWarning.set(true);
        this.pendingAction = null;
      } else if (this.pendingAction === 'new') {
        this.submitNewForm();
        this.pendingAction = null;
      }
    } else {
      this.pendingAction = null;
    }
  }

  // Métodos para el modal de modificación
  onModificationConfirm() {
    this.showModificationWarning.set(false);
    this.submitForm();
  }

  onModificationCancel() {
    this.showModificationWarning.set(false);
    this.submitAsNew();
  }

  submit() {
    if (!this.validateForm()) return;

    const validation = this.validationState();
    const hasInvalidTopics = !validation.main.isValid || !validation.sub.isValid || !validation.specific.isValid;

    if (hasInvalidTopics) {
      this.pendingAction = 'update';
      this.showTopicWarningModal.set(true);
    } else {
      this.showModificationWarning.set(true);
    }
  }

  // --- Guardado (helper genérico para update/create) ---

  private saveTest(request$: Observable<any>, successTitle?: string, successMsg?: string) {
    this.saving.set(true);

    request$.subscribe({
      next: (res: any) => {
        console.log('Test guardado con éxito:', res);
        this.saving.set(false);
        if (successTitle) this.successTitle.set(successTitle);
        if (successMsg) this.successMessage.set(successMsg);
        this.showSuccessModal.set(true);
      },
      error: (err) => {
        console.error('Error al guardar test:', err);
        this.saving.set(false);
        this.errorMessage.set(this.getErrorMessage(err));
        this.showErrorModal.set(true);
      }
    });
  }

  submitForm() {
    this.saveTest(this.testsManagementService.updateTest(this.testId, this.prepareFormData()));
  }

  submitAsNew() {
    if (!this.validateForm()) return;
    if (this.invalidTopics().length > 0) {
      this.pendingAction = 'new';
      this.showTopicWarningModal.set(true);
    } else {
      this.submitNewForm();
    }
  }

  submitNewForm() {
    const currentTitle = this.testForm.get('title')?.value || 'Test';
    const newTitle = this.generateNewTitle(currentTitle);
    const formData = this.prepareFormData({ includeIds: false, newTitle });

    this.saveTest(
      this.testsManagementService.createTest(formData),
      '¡Copia creada!',
      'La copia del test se ha creado correctamente.'
    );
  }

  private generateNewTitle(currentTitle: string): string {
    const now = new Date();
    const dateStr = now.toISOString().slice(0, 10);      // YYYY-MM-DD
    const timeStr = now.toTimeString().slice(0, 5);     // HH:mm
    return `${currentTitle} (copia ${dateStr} ${timeStr})`;
  }

  private markFormGroupTouched(formGroup: FormGroup | FormArray) {
    Object.values(formGroup.controls).forEach(control => {
      control.markAsTouched();

      if (control instanceof FormGroup || control instanceof FormArray) {
        this.markFormGroupTouched(control);
      }
    });
  }

  private prepareFormData(options: { includeIds?: boolean, newTitle?: string } = {}): any {
    const { newTitle } = options;
    const formValue = this.testForm.value;
    const title = newTitle || formValue.title.trim();

    const filteredQuestions = formValue.questions
      .filter((q: any) => q.question_text.trim())
      .map((question: any) => ({
        id: question.id || undefined,
        question_text: question.question_text.trim(),
        answers: question.answers
          .filter((a: any) => a.answer_text.trim())
          .map((answer: any) => ({
            id: answer.id || undefined,
            answer_text: answer.answer_text.trim(),
            is_correct: answer.is_correct
          }))
      }))
      .filter((q: any) => q.answers.length >= 2);

    return {
      title: title,
      description: formValue.description?.trim() || '',
      main_topic: formValue.main_topic,
      sub_topic: formValue.sub_topic,
      specific_topic: formValue.specific_topic,
      level: formValue.level,
      is_active: formValue.is_active,
      questions: filteredQuestions
    };
  }

  private getErrorMessage(err: any): string {
    if (err.error?.error) {
      return err.error.error;
    }

    const messages: Record<number, string> = {
      404: 'Test no encontrado.',
      401: 'No tienes permisos para editar este test.',
      400: 'Datos inválidos enviados.',
      500: 'Error del servidor. Intenta nuevamente más tarde.'
    };

    return messages[err.status] ?? 'Error desconocido al actualizar el test.';
  }

  private showError(message: string) {
    this.errorMessage.set(message);
    this.showErrorModal.set(true);
  }

  onSuccessModalConfirm() {
    this.showSuccessModal.set(false);
    this.router.navigate(['/admin/tests']);
  }

  onErrorModalConfirm() {
    this.showErrorModal.set(false);
  }

  cancel() {
    if (confirm('¿Estás seguro de que quieres cancelar? Los cambios no guardados se perderán.')) {
      this.router.navigate(['/admin/tests']);
    }
  }

  deleteQuestion(index: number) {
    if (confirm('¿Estás seguro de que quieres eliminar esta pregunta?')) {
      this.questions.removeAt(index);
    }
  }

  deleteAnswer(qIndex: number, aIndex: number) {
    if (this.getAnswers(qIndex).length <= 2) {
      alert('Debe haber al menos dos respuestas por pregunta.');
      return;
    }

    if (confirm('¿Estás seguro de que quieres eliminar esta respuesta?')) {
      this.getAnswers(qIndex).removeAt(aIndex);
    }
  }

  reload() {
    this.loadTest();
  }
}