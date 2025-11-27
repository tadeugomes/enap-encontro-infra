#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para adicionar seção Top 10 na página fase4.html
"""

# Ler o arquivo original
with open('docs/fase4.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Nova seção Top 10 a ser inserida após linha 184
top10_section = '''
        <section class="card" style="margin-top: 3rem; background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(245, 158, 11, 0.1)); border: 1px solid rgba(239, 68, 68, 0.3);">
            <h3><i class="fas fa-exclamation-triangle" style="color: #ef4444;"></i> Top 10 Casos de ALTO RISCO</h3>
            <p>Processos com maior desvio em relação ao valor esperado (acima do P90). Estes casos requerem auditoria prioritária.</p>
            
            <div style="overflow-x: auto; margin-top: 1.5rem;">
                <table style="width: 100%; border-collapse: collapse; font-size: 0.85rem;">
                    <thead>
                        <tr style="background: rgba(239, 68, 68, 0.2); border-bottom: 2px solid rgba(239, 68, 68, 0.4);">
                            <th style="padding: 0.75rem; text-align: left; font-weight: 600;">#</th>
                            <th style="padding: 0.75rem; text-align: left; font-weight: 600;">UF</th>
                            <th style="padding: 0.75rem; text-align: left; font-weight: 600;">Município</th>
                            <th style="padding: 0.75rem; text-align: left; font-weight: 600;">Tipo de Desastre</th>
                            <th style="padding: 0.75rem; text-align: right; font-weight: 600;">Valor Solicitado</th>
                            <th style="padding: 0.75rem; text-align: right; font-weight: 600;">Limite P90</th>
                            <th style="padding: 0.75rem; text-align: center; font-weight: 600;">Desvio</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                            <td style="padding: 0.75rem; color: #f59e0b; font-weight: bold;">1º</td>
                            <td style="padding: 0.75rem;">MT</td>
                            <td style="padding: 0.75rem;">Nova Monte Verde</td>
                            <td style="padding: 0.75rem; font-size: 0.8rem;">Chuvas Intensas</td>
                            <td style="padding: 0.75rem; text-align: right; font-weight: bold; color: #ef4444;">R$ 2,5 Bi</td>
                            <td style="padding: 0.75rem; text-align: right;">R$ 3,1 Mi</td>
                            <td style="padding: 0.75rem; text-align: center;"><span class="badge badge-danger">+235.559%</span></td>
                        </tr>
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                            <td style="padding: 0.75rem; color: #f59e0b; font-weight: bold;">2º</td>
                            <td style="padding: 0.75rem;">PE</td>
                            <td style="padding: 0.75rem;">Jaboatão Guararapes</td>
                            <td style="padding: 0.75rem; font-size: 0.8rem;">Chuvas Intensas</td>
                            <td style="padding: 0.75rem; text-align: right; font-weight: bold; color: #ef4444;">R$ 402 Mi</td>
                            <td style="padding: 0.75rem; text-align: right;">R$ 6,5 Mi</td>
                            <td style="padding: 0.75rem; text-align: center;"><span class="badge badge-danger">+29.867%</span></td>
                        </tr>
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                            <td style="padding: 0.75rem; color: #f59e0b; font-weight: bold;">3º</td>
                            <td style="padding: 0.75rem;">SP</td>
                            <td style="padding: 0.75rem;">Osasco</td>
                            <td style="padding: 0.75rem; font-size: 0.8rem;">Chuvas Intensas</td>
                            <td style="padding: 0.75rem; text-align: right; font-weight: bold; color: #ef4444;">R$ 268 Mi</td>
                            <td style="padding: 0.75rem; text-align: right;">R$ 13,3 Mi</td>
                            <td style="padding: 0.75rem; text-align: center;"><span class="badge badge-danger">+9.160%</span></td>
                        </tr>
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                            <td style="padding: 0.75rem; color: #f59e0b; font-weight: bold;">4º</td>
                            <td style="padding: 0.75rem;">RJ</td>
                            <td style="padding: 0.75rem;">Rio de Janeiro</td>
                            <td style="padding: 0.75rem; font-size: 0.8rem;">Chuvas Intensas</td>
                            <td style="padding: 0.75rem; text-align: right; font-weight: bold; color: #ef4444;">R$ 172 Mi</td>
                            <td style="padding: 0.75rem; text-align: right;">R$ 7,2 Mi</td>
                            <td style="padding: 0.75rem; text-align: center;"><span class="badge badge-danger">+10.220%</span></td>
                        </tr>
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                            <td style="padding: 0.75rem; color: #f59e0b; font-weight: bold;">5º</td>
                            <td style="padding: 0.75rem;">GO</td>
                            <td style="padding: 0.75rem;">Anápolis</td>
                            <td style="padding: 0.75rem; font-size: 0.8rem;">Chuvas Intensas</td>
                            <td style="padding: 0.75rem; text-align: right; font-weight: bold; color: #ef4444;">R$ 169 Mi</td>
                            <td style="padding: 0.75rem; text-align: right;">R$ 12,0 Mi</td>
                            <td style="padding: 0.75rem; text-align: center;"><span class="badge badge-danger">+3.078%</span></td>
                        </tr>
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                            <td style="padding: 0.75rem; color: #f59e0b; font-weight: bold;">6º</td>
                            <td style="padding: 0.75rem;">RJ</td>
                            <td style="padding: 0.75rem;">Barra Mansa</td>
                            <td style="padding: 0.75rem; font-size: 0.8rem;">Chuvas Intensas</td>
                            <td style="padding: 0.75rem; text-align: right; font-weight: bold; color: #ef4444;">R$ 127 Mi</td>
                            <td style="padding: 0.75rem; text-align: right;">R$ 6,3 Mi</td>
                            <td style="padding: 0.75rem; text-align: center;"><span class="badge badge-danger">+7.521%</span></td>
                        </tr>
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                            <td style="padding: 0.75rem; color: #f59e0b; font-weight: bold;">7º</td>
                            <td style="padding: 0.75rem;">PE</td>
                            <td style="padding: 0.75rem;">Ipojuca</td>
                            <td style="padding: 0.75rem; font-size: 0.8rem;">Enxurradas</td>
                            <td style="padding: 0.75rem; text-align: right; font-weight: bold; color: #ef4444;">R$ 112 Mi</td>
                            <td style="padding: 0.75rem; text-align: right;">R$ 5,3 Mi</td>
                            <td style="padding: 0.75rem; text-align: center;"><span class="badge badge-danger">+4.941%</span></td>
                        </tr>
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                            <td style="padding: 0.75rem; color: #f59e0b; font-weight: bold;">8º</td>
                            <td style="padding: 0.75rem;">RS</td>
                            <td style="padding: 0.75rem;">Roca Sales</td>
                            <td style="padding: 0.75rem; font-size: 0.8rem;">Chuvas Intensas</td>
                            <td style="padding: 0.75rem; text-align: right; font-weight: bold; color: #ef4444;">R$ 109 Mi</td>
                            <td style="padding: 0.75rem; text-align: right;">R$ 6,3 Mi</td>
                            <td style="padding: 0.75rem; text-align: center;"><span class="badge badge-danger">+9.058%</span></td>
                        </tr>
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                            <td style="padding: 0.75rem; color: #f59e0b; font-weight: bold;">9º</td>
                            <td style="padding: 0.75rem;">PE</td>
                            <td style="padding: 0.75rem;">Grupo municípios</td>
                            <td style="padding: 0.75rem; font-size: 0.8rem;">Enxurradas</td>
                            <td style="padding: 0.75rem; text-align: right; font-weight: bold; color: #ef4444;">R$ 106 Mi</td>
                            <td style="padding: 0.75rem; text-align: right;">R$ 7,2 Mi</td>
                            <td style="padding: 0.75rem; text-align: center;"><span class="badge badge-danger">+2.260%</span></td>
                        </tr>
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                            <td style="padding: 0.75rem; color: #f59e0b; font-weight: bold;">10º</td>
                            <td style="padding: 0.75rem;">BA</td>
                            <td style="padding: 0.75rem;">Itabuna</td>
                            <td style="padding: 0.75rem; font-size: 0.8rem;">Chuvas Intensas</td>
                            <td style="padding: 0.75rem; text-align: right; font-weight: bold; color: #ef4444;">R$ 104 Mi</td>
                            <td style="padding: 0.75rem; text-align: right;">R$ 47,2 Mi</td>
                            <td style="padding: 0.75rem; text-align: center;"><span class="badge badge-danger">+1.334%</span></td>
                        </tr>
                    </tbody>
                </table>
            </div>
            
            <div style="margin-top: 1.5rem; padding: 1rem; background: rgba(0,0,0,0.2); border-radius: 0.5rem; border-left: 3px solid #ef4444;">
                <p style="font-size: 0.85rem; margin: 0;"><i class="fas fa-info-circle" style="color: #ef4444; margin-right: 0.5rem;"></i>
                    <strong>Destaque:</strong> O caso #1 (Nova Monte Verde-MT) apresenta um pedido de <strong>R$ 2,5 bilhões</strong>, 
                    valor 79.830x superior ao limite esperado. Este caso demonstra a import ância de mecanismos automatizados de triagem.
                </p>
            </div>
        </section>

'''

# Inserir a nova seção após a linha 184 (índice 183 em Python, pois começa em 0)
# Linha 184 é "</section>" do "Resultados da Análise"
# Precisamos inserir antes da linha 186 que é "<section class="grid grid-2">"

# Encontrar a posição correta (linha 185 é vazia, linha 186 começa nova section)
insert_position = 185  # Após linha 184 (</section>) e linha vazia 185

# Criar novo conteúdo
new_lines = lines[:insert_position] + [top10_section] + lines[insert_position:]

# Salvar o arquivo
with open('docs/fase4.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("✅ Seção Top 10 adicionada com sucesso em docs/fase4.html")
print(f"   Inserida na posição: linha {insert_position + 1}")
