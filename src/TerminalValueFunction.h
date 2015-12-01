#ifndef TerminalValueFunction_h
#define TerminalValueFunction_h

#include "ValueFunction.h"

class TerminalValueFunction : public ValueFunction
{

public:

  std::shared_ptr<State> prior;

  TerminalValueFunction(std::shared_ptr<State> prior) : prior(prior) { }

  inline virtual double Evaluate(std::shared_ptr<State> state) override
  {
    return state->GetKL(prior);
  }

  inline virtual void Train(const std::vector<std::shared_ptr<State>> states, const Eigen::VectorXd& costs) override
  {
    // pass
  }

};

#endif // ifndef TerminalValueFunction_h
