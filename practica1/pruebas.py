from apscheduler.schedulers.background import BackgroundScheduler
from controllers.loteControl import LoteControl

def run_scheduler():
    lote_control = LoteControl()

    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(lote_control.actualizarEstadoLotes, 'interval', minutes=1)  # Ejecutar cada minuto
    
    # Aquí podrías añadir impresiones para asegurarte de que el planificador está funcionando
    print("El planificador está en funcionamiento.")

    # No es necesario llamar a actualizarEstadoLotes aquí
    # La función se ejecutará automáticamente según la configuración del planificador

if __name__ == "__main__":
    run_scheduler()
    # No coloques ningún código aquí que quieras que se ejecute después de run_scheduler
