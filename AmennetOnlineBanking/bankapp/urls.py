from django.urls import path
from . import views
urlpatterns = [
    path('form/',views.form,name='form'),
    path('plus/', views.plus,name='plus'),#urlpatterns = [
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('recherchemouvement/', views.recherchemouvement_view, name='recherchemouvement'),
    path('mvmparop/', views.mvmparop_view, name='mvmparop'),
    path('cfonbparcompteparperiode/', views.cfonbparcompteparperiode_view, name='cfonbparcompteparperiode'),
    path('cfonbhis/', views.cfonbhis_view, name='cfonbhis'),
    path('cfonbhisglobal/', views.cfonbhisglobal_view, name='cfonbhisglobal'),
    path('settings/', views.settings, name='settings'),
    path('setprfr/', views.setprfr, name='setprfr'),
    path('setprfrlib/', views.setprfrlib, name='setprfrlib'),
    path('setprfrmail/', views.setprfrmail, name='setprfrmail'),
    path('setprfrsms/', views.setprfrsms, name='setprfrsms'),
    path('setprfrcompteur/', views.setprfrcompteur, name='setprfrcompteur'),
    path('setmail/', views.setmail, name='setmail'),
    path('setinf/', views.setinf, name='setinf'),
    path('security/', views.security, name='security'),
    path('virement/', views.virement, name='virement'),
    path('virmentsigne/', views.virmentsigne_view, name='virmentsigne'),
    path('virhis/', views.virhis_view, name='virhis'),
    path('virben/', views.virben_view, name='virben'),
    path('virbenges/', views.virbenges_view, name='virbenges'),
    path('virbensin/', views.virbensin_view, name='virbensin'),
    path('virbenhis/', views.virbenhis_view, name='virbenhis'),
    path('virmas/', views.virmas_view, name='virmas'),
    path('virmassin/', views.virmassin_view, name='virmassin'),
    path('virmashis/', views.virmashis_view, name='virmashis'),
    path('virper/', views.virper_view, name='virper'),
    path('virperben/', views.virperben_view, name='virperben'),
    path('virperlis/', views.virperlis_view, name='virperlis'),
    path('virpersin/', views.virpersin_view, name='virpersin'),
    path('modvir/', views.modvir_view, name='modvir'),
    path('mon/', views.mon_view, name='mon'),
    path('monrech/', views.monrech_view, name='monrech'),
    path('mondeb/', views.mondeb_view, name='mondeb'),
    path('monopp/', views.monopp_view, name='monopp'),
    path('tele.html', views.ouverture_lc_view, name='tele'),
    path('telete/', views.transfert_emis_tre_view, name='telete'),
    path('teletr/', views.transfert_recus_trr_view, name='teletr'),
    path('teleaop/', views.avis_operation_pdf_view, name='teleaop'),
    path('teleaot/', views.avis_operation_text_view, name='teleaot'),
    path('telees/', views.situation_effets_view, name='telees'),
    path('telecro/', views.cro_effet_structured_view, name='telecro'),
    path('telercp/', views.releve_compte_pdf_view, name='telercp'),
    path('telerct/', views.releve_compte_text_view, name='telerct'),
    path('telercc/', views.releve_compte_cfonb_view, name='telercc'),
    path('teleeip/', views.echelle_interets_pdf_view, name='teleeip'),
    path('teleeit/', views.echelle_interets_text_view, name='teleeit'),
    path('teleic/', views.image_cheques_view, name='teleic'),
    path('teleil/', views.image_lettres_change_view, name='teleil'),
    path('telescard/', views.situation_cartes_view, name='telescard'),
    path('telescred/', views.situation_credits_view, name='telescred'),
    path('telesplac/', views.situation_placements_view, name='telesplac'),
    path('telesorcheq/', views.sort_cheques_verse_view, name='telesorcheq'),
    path('teletrantpe/', views.transactions_tpe_view, name='teletrantpe'),
    path('teled/', views.divers_view, name='teled'),
    path('mes/', views.rediger_message_agence, name='mes'),
    path('messuppo/', views.rediger_message_support, name='messuppo'),
    path('mesrec/', views.messages_recus, name='mesrec'),
    path('mesenv/', views.messages_envoyes, name='mesenv'),
    path('mesins/', views.messages_en_instance, name='mesins'),
    path('messupp./', views.messages_supprimes, name='messupp'),
    path('fin./', views.fin, name='fin'),
    path('finsc/', views.finsc, name='finsc'),
    path('cd/', views.cd, name='cd'),
    path('cbam/', views.cbam, name='cbam'),
    path('cs./', views.cs, name='cs'),
    path('cb/', views.cb, name='cb'),
    path('gb/', views.gb, name='gb'),
    path('gbc/', views.gbc, name='gbc'),
    path('gbdr/', views.gbdr, name='gbdr'),
    path('gbed/', views.gbed, name='gbed'),
    path('services/', views.services_view, name='services'),
    path('spi/', views.spi_view, name='spi'),
    path('sst/', views.sst_view, name='sst'),
    path('scch/', views.scch_view, name='scch'),
    path('sdc/', views.sdc_view, name='sdc'),
    path('sdml/', views.sdml_view, name='sdml'),
    path('sdd/', views.sdd_view, name='sdd'),
    path('etr/', views.ordre_virement_view, name='etr'),
    path('etrsin/', views.transfert_emis_signer_view, name='etrsin'),
    path('etrhis/', views.historique_transferts_emis_view, name='etrhis'),
    path('etrcrd/', views.ouverture_lettre_credit_view, name='etrcrd'),
    path('etrcrdsin/', views.lettres_credit_signer_view, name='etrcrdsin'),
    path('etrcrdhis/', views.historique_lettres_credit_view, name='etrcrdhis'),
]