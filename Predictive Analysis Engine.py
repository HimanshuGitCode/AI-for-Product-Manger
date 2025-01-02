class CompetitorPredictor:
    def __init__(self, historical_data: pd.DataFrame):
        self.historical_data = historical_data
        self.predictions = {}
    
    def predict_next_moves(self, competitor: str):
        """Predict likely next moves for a competitor"""
        # Get competitor's historical patterns
        competitor_data = self.historical_data[
            self.historical_data['competitor'] == competitor
        ]
        
        # Analyze patterns with GPT-4
        analysis_prompt = self._create_analysis_prompt(competitor_data)
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a strategic analyst predicting competitor moves based on historical patterns."},
                {"role": "user", "content": analysis_prompt}
            ]
        )
        
        # Structure predictions
        self.predictions[competitor] = {
            'likely_moves': self._parse_predictions(response.choices[0].message.content),
            'confidence_score': self._calculate_confidence(competitor_data),
            'prediction_date': datetime.now().isoformat()
        }
        
        return self.predictions[competitor]
    
    def _create_analysis_prompt(self, data: pd.DataFrame) -> str:
        """Create detailed prompt for GPT-4 analysis"""
        return f"""
        Based on this historical data:
        
        Recent Actions:
        {data['actions'].tail(5).to_string()}
        
        Market Changes:
        {data['market_changes'].tail(5).to_string()}
        
        Product Updates:
        {data['product_updates'].tail(5).to_string()}
        
        Predict:
        1. Most likely next product moves
        2. Potential pricing changes
        3. Market positioning shifts
        4. Timeline for these changes
        """
