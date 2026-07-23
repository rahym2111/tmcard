import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    # Render serweriniň hödürleýän PORT üýtgeýänini alýarys (bolmasa 5000)
    port = int(os.environ.get('PORT', 5000))
    
    # host='0.0.0.0' Render-iň porty daşaryga açmagy üçin MÜTLEM GEREK!
    app.run(host='0.0.0.0', port=port)
