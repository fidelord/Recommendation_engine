from flask import Flask, request, jsonify
from fetching_investments import content_based_recommendations, build_chart

app = Flask(__name__)



# Endpoint to recommend similar movies based on a given movie title
@app.route('/recommend', methods=['GET'])
def recommend_movies():
    Investment_product = request.args.get('investment_product')
    Category = request.args.getlist('category')

    if Investment_product is None and Category is None:
        return  jsonify({'error': 'Needed parameters not provided'}), 400
    elif Investment_product:
        investment = content_based_recommendations(Investment_product)
        return jsonify({'recommendations': investment})
    elif Category:
        investment = build_chart(Category)
        return jsonify({'recommendations': investment})
    
if __name__ == '__main__':
    app.run(debug=True)
