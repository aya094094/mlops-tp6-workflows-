from flow_mlops import reentrainement

if __name__ == '__main__':
    # Cree le deploiement "hebdomadaire" puis attend les executions a lancer.
    # Laisser ce terminal ouvert ; Ctrl + C pour arreter.
    reentrainement.serve(name='hebdomadaire',
                         cron='0 6 * * 1')          # chaque lundi a 6 h
