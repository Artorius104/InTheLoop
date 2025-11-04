"""
InTheLoop - Interface Streamlit
Application de veille scientifique intelligente
"""
import streamlit as st
import requests
import time
from datetime import datetime
from typing import Optional, Dict, Any

# Configuration
API_BASE_URL = "http://localhost:8000/api"

# Configuration de la page
st.set_page_config(
    page_title="InTheLoop - Veille Scientifique",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
    }
</style>
""", unsafe_allow_html=True)


def check_api_health() -> bool:
    """Vérifie si l'API backend est accessible"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False


def create_research(topic: str, sources: list, max_results: int = 10) -> Optional[Dict[str, Any]]:
    """Crée une nouvelle recherche"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/research/",
            json={
                "topic": topic,
                "sources": sources,
                "max_results_per_source": max_results
            },
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Erreur lors de la création de la recherche : {str(e)}")
        return None


def get_research(research_id: int) -> Optional[Dict[str, Any]]:
    """Récupère les détails d'une recherche"""
    try:
        response = requests.get(f"{API_BASE_URL}/research/{research_id}", timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Erreur lors de la récupération : {str(e)}")
        return None


def list_researches() -> list:
    """Liste toutes les recherches"""
    try:
        response = requests.get(f"{API_BASE_URL}/research/", timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Erreur lors de la récupération de l'historique : {str(e)}")
        return []


def display_research_results(research: Dict[str, Any]):
    """Affiche les résultats d'une recherche"""
    
    # Statut
    status_colors = {
        "pending": "🟡",
        "in_progress": "🔵", 
        "completed": "🟢",
        "failed": "🔴"
    }
    
    status_icon = status_colors.get(research["status"], "⚪")
    st.markdown(f"### {status_icon} Statut : {research['status'].upper()}")
    
    # Informations temporelles
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Créée le :** {research['created_at'][:19]}")
    with col2:
        if research.get('completed_at'):
            st.write(f"**Terminée le :** {research['completed_at'][:19]}")
    
    # Si la recherche est terminée, afficher les résultats
    if research["status"] == "completed" and research.get("results"):
        results = research["results"]
        
        # Statistiques
        st.markdown("---")
        st.markdown("### 📊 Statistiques")
        
        if results.get("metadata"):
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Résultats totaux", results["metadata"].get("total_results", 0))
            with col2:
                st.metric("Sources consultées", results["metadata"].get("total_sources", 0))
        
        # Résumé exécutif
        if results.get("report", {}).get("executive_summary"):
            st.markdown("---")
            st.markdown("### 📝 Résumé Exécutif")
            st.info(results["report"]["executive_summary"])
        
        # Découvertes clés
        if results.get("report", {}).get("insights"):
            st.markdown("---")
            st.markdown("### 💡 Découvertes Clés")
            for insight in results["report"]["insights"]:
                st.markdown(f"- ✅ {insight}")
        
        # Top articles
        if results.get("report", {}).get("top_papers"):
            st.markdown("---")
            st.markdown("### 📚 Top Articles")
            
            for i, paper in enumerate(results["report"]["top_papers"][:5], 1):
                with st.expander(f"{i}. {paper.get('title', 'Sans titre')}"):
                    if paper.get('authors'):
                        authors = paper['authors'][:3] if isinstance(paper['authors'], list) else [paper['authors']]
                        st.write(f"**Auteurs :** {', '.join(authors)}")
                    
                    if paper.get('abstract'):
                        st.write(f"**Résumé :** {paper['abstract'][:500]}...")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if paper.get('citations'):
                            st.write(f"📊 {paper['citations']} citations")
                    with col2:
                        if paper.get('published_date'):
                            st.write(f"📅 {paper['published_date']}")
                    with col3:
                        if paper.get('url'):
                            st.markdown(f"[🔗 Voir l'article]({paper['url']})")
        
        # Recommandations
        if results.get("report", {}).get("recommendations"):
            st.markdown("---")
            st.markdown("### 🎯 Recommandations")
            for rec in results["report"]["recommendations"]:
                st.markdown(f"- 💡 {rec}")
    
    elif research["status"] == "failed":
        st.error(f"❌ Erreur : {research.get('error', 'Erreur inconnue')}")


def main():
    """Application principale"""
    
    # En-tête
    st.markdown('<h1 class="main-header">🔬 InTheLoop</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Veille Scientifique Intelligente</p>', unsafe_allow_html=True)
    
    # Vérification de l'API
    if not check_api_health():
        st.error("⚠️ Le backend n'est pas accessible. Assurez-vous qu'il est démarré sur http://localhost:8000")
        st.info("Lancez le backend avec : `cd backend && source venv/bin/activate && uvicorn main:app --reload`")
        return
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🎯 Navigation")
        page = st.radio("", ["🔍 Nouvelle Recherche", "📜 Historique"], label_visibility="collapsed")
        
        st.markdown("---")
        st.markdown("### ℹ️ À propos")
        st.markdown("""
        **InTheLoop** utilise un framework agentic pour rechercher, analyser et synthétiser l'information scientifique.
        
        **Sources disponibles :**
        - arXiv (preprints)
        - Semantic Scholar
        - Wikipedia
        - Actualités scientifiques
        """)
    
    # Page : Nouvelle Recherche
    if page == "🔍 Nouvelle Recherche":
        st.markdown("## 🔍 Nouvelle Recherche")
        
        # Formulaire
        with st.form("research_form"):
            topic = st.text_input(
                "Sujet de recherche",
                placeholder="Ex: Large Language Models architectures",
                help="Entrez le sujet scientifique que vous souhaitez explorer"
            )
            
            st.markdown("### Sources à interroger")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                arxiv = st.checkbox("arXiv", value=True)
                semantic = st.checkbox("Semantic Scholar", value=True)
            with col2:
                wiki = st.checkbox("Wikipedia", value=True)
                news = st.checkbox("Actualités", value=False)
            with col3:
                web = st.checkbox("Web Search", value=False)
            
            max_results = st.slider("Résultats par source", 5, 20, 10)
            
            submitted = st.form_submit_button("🚀 Lancer la recherche", use_container_width=True)
        
        if submitted:
            if not topic.strip():
                st.warning("⚠️ Veuillez entrer un sujet de recherche")
            else:
                # Préparer les sources
                sources = []
                if arxiv: sources.append("arxiv")
                if semantic: sources.append("semantic_scholar")
                if wiki: sources.append("wikipedia")
                if news: sources.append("news")
                if web: sources.append("web_search")
                
                if not sources:
                    st.warning("⚠️ Veuillez sélectionner au moins une source")
                else:
                    with st.spinner("🔄 Création de la recherche..."):
                        research = create_research(topic, sources, max_results)
                    
                    if research:
                        st.success(f"✅ Recherche #{research['id']} créée avec succès !")
                        
                        # Polling pour suivre la progression
                        progress_bar = st.progress(0)
                        status_placeholder = st.empty()
                        
                        max_wait = 120  # 2 minutes max
                        elapsed = 0
                        
                        while elapsed < max_wait:
                            research_data = get_research(research['id'])
                            
                            if research_data:
                                status = research_data['status']
                                status_placeholder.info(f"📊 Statut : {status}")
                                
                                if status == "completed":
                                    progress_bar.progress(100)
                                    status_placeholder.success("✅ Recherche terminée !")
                                    time.sleep(1)
                                    st.markdown("---")
                                    display_research_results(research_data)
                                    break
                                elif status == "failed":
                                    progress_bar.progress(100)
                                    status_placeholder.error("❌ La recherche a échoué")
                                    st.error(f"Erreur : {research_data.get('error', 'Erreur inconnue')}")
                                    break
                                elif status == "in_progress":
                                    progress = min(50 + (elapsed * 2), 90)
                                    progress_bar.progress(progress)
                            
                            time.sleep(2)
                            elapsed += 2
                        
                        if elapsed >= max_wait:
                            st.warning("⏱️ Temps d'attente dépassé. La recherche continue en arrière-plan.")
                            st.info(f"Consultez l'historique pour voir les résultats (ID: {research['id']})")
        
        # Exemples
        st.markdown("---")
        st.markdown("### 💡 Exemples de sujets")
        examples = [
            "Neural networks for natural language processing",
            "Quantum computing applications in cryptography",
            "CRISPR gene editing recent advances",
            "Transformer architecture improvements",
        ]
        
        cols = st.columns(2)
        for i, example in enumerate(examples):
            with cols[i % 2]:
                if st.button(example, key=f"example_{i}", use_container_width=True):
                    st.session_state['example_topic'] = example
                    st.rerun()
    
    # Page : Historique
    else:
        st.markdown("## 📜 Historique des Recherches")
        
        researches = list_researches()
        
        if not researches:
            st.info("Aucune recherche pour le moment. Créez-en une pour commencer !")
        else:
            for research in researches:
                with st.expander(f"#{research['id']} - {research['topic'][:60]}... ({research['status']})"):
                    research_data = get_research(research['id'])
                    if research_data:
                        display_research_results(research_data)


if __name__ == "__main__":
    main()

