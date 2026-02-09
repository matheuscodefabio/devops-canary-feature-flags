# devops-canary-feature-flags

### **Progressive Delivery Platform no Kubernetes**

com **Feature Flags, Canary Release, Observabilidade e Rollback automático**

Nome vendável:

> **“Building a Production-Grade Progressive Delivery Platform on Kubernetes”**
> 

---

## 🔥 O que deixa isso fora da curva

Não é só subir ferramenta. É **resolver problema real de produção**:

- Deploy sem derrubar usuário
- Medir impacto de feature nova
- Ativar/desativar funcionalidade sem novo deploy
- Fazer rollback automático baseado em métrica

---

## 🧱 Arquitetura (alto nível)

```
Dev → GitHub → GitHub Actions
        ↓
     Build Image
        ↓
      Argo Rollouts (Canary)
        ↓
   Kubernetes (EKS / Kind)
        ↓
 ┌───────────────┐
 │  Aplicação    │
 │  (Spring /    │
 │   Node / Go)  │
 └──────┬────────┘
        │
  ┌─────▼─────┐
  │ Feature   │  ← Flipper
  │ Flags     │
  └─────┬─────┘
        │
┌───────▼────────┐
│ Observability  │
│ Prometheus     │
│ Grafana        │
│ Loki           │
│ Tempo (opcional)│
└────────────────┘
```

---

## 🧠 Stack sugerida (intencional)

### Core

- Kubernetes (kind local + desenho pensando em EKS)
- Helm
- GitHub Actions
- Argo Rollouts

### Feature Flag

- **Flipper**
- Flag avaliada em runtime pela app
- Flag controlando comportamento real (ex: novo endpoint, novo cálculo, novo layout)

### Observabilidade

- Prometheus
- Grafana
- Loki (logs)
- Opcional: Tempo (trace)

### App

- Algo simples, mas real:
    - API REST com:
        - `/checkout`
        - `/price`
        - `/recommendation`

A feature flag muda o comportamento da resposta.

---

## 🚀 Fluxo real de produção

1. Dev cria PR
2. GitHub Actions:
    - Build da imagem
    - Testes
    - Push no registry
3. Argo Rollouts:
    - Canary 10% → 30% → 50%
4. Prometheus avalia:
    - Latência
    - Error rate
5. Se piorar:
    - **Rollback automático**
6. Feature flag:
    - Ligada apenas para 10% dos usuários
    - Sem redeploy

Isso é **nível empresa grande**.

---

## 📊 Dashboards que impressionam

No Grafana:

- Latência por versão (canary vs stable)
- Error rate por feature flag
- Requests por pod
- Flag ON vs OFF impactando métrica

Isso é ouro para LinkedIn.
