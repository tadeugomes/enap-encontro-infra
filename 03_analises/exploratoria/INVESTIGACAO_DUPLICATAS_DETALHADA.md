# 🔍 Investigação Detalhada das Duplicatas Removidas

**Data**: 22/11/2025  
**Objetivo**: Verificar se duplicatas tinham informações diferentes

---

## 📊 Resultados

### Duplicatas Analisadas:
- **Total de registros duplicados**: 302
- **Códigos IBGE duplicados**: 149
- **Duplicatas EXATAS**: 0
- **Duplicatas PARCIAIS**: 302
- **Casos com diferenças**: 20

---

## ⚠️ ALERTA


### ⚠️ PROBLEMA IDENTIFICADO

**20 casos têm informações DIFERENTES entre as duplicatas!**

Isso significa que:
1. Não eram duplicatas verdadeiras
2. Podem representar informações distintas do mesmo município
3. A remoção pode ter causado **PERDA DE DADOS**

### Casos com Diferenças:

1. **AC/Sena Madureira** (Código: 1200500.0)
   - Duplicatas: 2
   - Colunas diferentes: Metrica_5, Porte, Classificacao_4, Faixa_ICM

2. **AM/Amaturá** (Código: 1300060.0)
   - Duplicatas: 2
   - Colunas diferentes: Metrica_5, Porte, Classificacao_4, Faixa_ICM

3. **AM/Apuí** (Código: 1300144.0)
   - Duplicatas: 2
   - Colunas diferentes: Metrica_5, Porte, Classificacao_4, Faixa_ICM

4. **AM/Novo Airão** (Código: 1303205.0)
   - Duplicatas: 2
   - Colunas diferentes: Metrica_5, Porte, Classificacao_4, Faixa_ICM

5. **AM/Urucará** (Código: 1304302.0)
   - Duplicatas: 2
   - Colunas diferentes: Metrica_5, Porte, Classificacao_4, Faixa_ICM

6. **PA/Abaetetuba** (Código: 1500107.0)
   - Duplicatas: 2
   - Colunas diferentes: Metrica_5, Porte, Classificacao_4, Faixa_ICM

7. **PA/Água Azul do Norte** (Código: 1500347.0)
   - Duplicatas: 2
   - Colunas diferentes: Metrica_5, Porte, Classificacao_4, Faixa_ICM

8. **PA/Brasil Novo** (Código: 1501725.0)
   - Duplicatas: 2
   - Colunas diferentes: Metrica_5, Metrica_12, Porte, Prioridade, Classificacao_4, Faixa_ICM

9. **PA/Curuá** (Código: 1502855.0)
   - Duplicatas: 2
   - Colunas diferentes: Metrica_5, Porte, Classificacao_4, Faixa_ICM

10. **PA/Gurupá** (Código: 1503101.0)
   - Duplicatas: 2
   - Colunas diferentes: Metrica_5, Porte, Classificacao_4, Faixa_ICM

11. **PA/Santa Luzia do Pará** (Código: 1506559.0)
   - Duplicatas: 2
   - Colunas diferentes: Metrica_5, Metrica_18, Porte, Classificacao_3, Classificacao_4, Faixa_ICM

12. **PA/Senador José Porfírio** (Código: 1507805.0)
   - Duplicatas: 2
   - Colunas diferentes: Metrica_5, Porte, Classificacao_4, Faixa_ICM

13. **PA/Tucumã** (Código: 1508084.0)
   - Duplicatas: 2
   - Colunas diferentes: Metrica_5, Porte, Classificacao_4, Faixa_ICM

14. **PA/Ulianópolis** (Código: 1508126.0)
   - Duplicatas: 2
   - Colunas diferentes: Metrica_4, Metrica_15, Metrica_16, Porte, Classificacao_3, Classificacao_4, Faixa_ICM

15. **PA/Uruará** (Código: 1508159.0)
   - Duplicatas: 2
   - Colunas diferentes: Metrica_5, Porte, Classificacao_4, Faixa_ICM

16. **PA/Viseu** (Código: 1508308.0)
   - Duplicatas: 2
   - Colunas diferentes: Metrica_5, Porte, Classificacao_4, Faixa_ICM

17. **TO/Formoso do Araguaia** (Código: 1708205.0)
   - Duplicatas: 2
   - Colunas diferentes: Metrica_5, Porte, Classificacao_4, Faixa_ICM

18. **TO/Muricilândia** (Código: 1713957.0)
   - Duplicatas: 2
   - Colunas diferentes: Metrica_14, Prioridade, Classificacao_4, Faixa_ICM

19. **TO/São Miguel do Tocantins** (Código: 1720200.0)
   - Duplicatas: 2
   - Colunas diferentes: Metrica_5, Porte, Classificacao_4, Faixa_ICM

20. **MA/Bom Jardim** (Código: 2102002.0)
   - Duplicatas: 2
   - Colunas diferentes: Metrica_6, Metrica_15, Metrica_18, Porte, Classificacao_3, Classificacao_4, Faixa_ICM


---

## 🎯 RECOMENDAÇÕES URGENTES

1. ❌ **REVERTER a limpeza de duplicatas**
2. ✅ **INVESTIGAR cada caso** individualmente
3. ✅ **MANTER todas as ocorrências** se houver diferenças
4. ✅ **Remover apenas duplicatas EXATAS** (todas as colunas iguais)

### Próximos Passos:
1. Analisar as colunas que diferem
2. Entender o significado das diferenças
3. Decidir critério de desduplicação correto
4. Refazer limpeza com critério adequado

---

**Status**: ⚠️ REQUER AÇÃO IMEDIATA
