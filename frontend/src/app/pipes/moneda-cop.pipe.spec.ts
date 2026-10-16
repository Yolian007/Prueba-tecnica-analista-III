import { MonedaCopPipe } from './moneda-cop.pipe';

describe('MonedaCopPipe', () => {
  const pipe = new MonedaCopPipe();

  it('formatea valores numéricos como pesos colombianos', () => {
    const resultado = pipe.transform('1190000.00');
    expect(resultado).toContain('$');
    expect(resultado).toContain('1.190.000');
  });

  it('muestra guion para valores vacíos', () => {
    expect(pipe.transform('')).toBe('—');
    expect(pipe.transform(null)).toBe('—');
  });

  it('devuelve el texto original si no es numérico', () => {
    expect(pipe.transform('abc')).toBe('abc');
  });
});
