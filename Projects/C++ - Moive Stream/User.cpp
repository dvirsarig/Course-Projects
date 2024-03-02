
#include "User.h"
#include "RecommendationSystem.h"
// Constructor
User::User (std::string& name, rank_map& ranks,
            std::shared_ptr<RecommendationSystem>& rec_system): user_name
            (name), user_ranks(ranks), user_rec_system(rec_system)
{}

std::string User::get_name() const{ // Return username.
  return user_name;
}

void User::add_movie_to_rs(const std::string &name, int year,
                     const std::vector<double> &features,
                     double rate){
  // Add new movie to the user recommendation system
  // need to add the rade to the rank map??????*****
  user_rec_system->add_movie (name, year, features);
  sp_movie the_movie = user_rec_system->get_movie (name, year);
  std::pair<sp_movie , double> new_pair = std::make_pair (the_movie, rate);
  user_ranks.insert (new_pair);
}

rank_map User::get_ranks() const{ // Return the ranks of the user.
  return user_ranks;
}

sp_movie User::get_recommendation_by_content() const{
  // The function activate algorithm that calculate the recommendation by
  // content of a movie and return it.
  return user_rec_system->recommend_by_content (*this);
}

sp_movie User::get_recommendation_by_cf(int k) const{
  // The function activate algorithm that calculate the recommendation by
  // ranks of the user for other movies and return a movie.
  return user_rec_system->recommend_by_cf (*this, k);
}

double User::get_prediction_score_for_movie(const std::string& name, int year,
                                       int k) const{
  // Get the pointer to the movie and checks if it is the system.
  sp_movie movie = user_rec_system->get_movie (name, year);
  if (movie == nullptr){
    throw std::runtime_error("There is no movie with those name and year");
  }
  // Activate the algorithm and return the result.
  return user_rec_system->predict_movie_score (*this, movie, k);
}

std::ostream& operator<<(std::ostream& s, const User& user){
  s << "name: " << user.user_name << "\n" << *(user.user_rec_system);
  return s;
}
