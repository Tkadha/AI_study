#include "MinerOwnedStates.h"
#include "State.h"
#include "Miner.h"
#include "Locations.h"
#include "misc/ConsoleUtils.h"
#include "EntityNames.h"

#include <iostream>
using std::cout;

//define this to output to a file
#ifdef TEXTOUTPUT
#include <fstream>
extern std::ofstream os;
#define cout os
#endif





//--------------------------------------methods for EnterMineAndDigForNugget

EnterMineAndDigForNugget* EnterMineAndDigForNugget::Instance()
{
  static EnterMineAndDigForNugget instance;

  return &instance;
}

void EnterMineAndDigForNugget::Enter(Miner* pMiner)
{
  //if the miner is not already located at the goldmine, he must
  //change location to the gold mine
    if (pMiner->Havefish()) {
        pMiner->Eatfish();
        SetTextColor(FOREGROUND_BLUE | FOREGROUND_INTENSITY);
        cout << "\n" << GetNameOfEntity(pMiner->ID()) << ": " << "Eat fish";
    }
  if (pMiner->Location() != goldmine)
  {
    SetTextColor(FOREGROUND_BLUE| FOREGROUND_INTENSITY);
    cout << "\n" << GetNameOfEntity(pMiner->ID()) << ": " << "Walkin' to the goldmine";

    pMiner->ChangeLocation(goldmine);
  }
}


void EnterMineAndDigForNugget::Execute(Miner* pMiner)
{  
  //the miner digs for gold until he is carrying in excess of MaxNuggets. 
  //If he gets thirsty during his digging he packs up work for a while and 
  //changes state to go to the saloon for a whiskey.
  pMiner->AddToGoldCarried(1);

  pMiner->IncreaseFatigue();

  SetTextColor(FOREGROUND_BLUE | FOREGROUND_INTENSITY);
  cout << "\n" << GetNameOfEntity(pMiner->ID()) << ": " << "Pickin' up a nugget";

  //if enough gold mined, go and put it in the bank
  if (pMiner->PocketsFull())
  {
    pMiner->ChangeState(VisitBankAndDepositGold::Instance());
  }

  if (pMiner->Thirsty())
  {
    pMiner->ChangeState(QuenchThirst::Instance());
  }
}


void EnterMineAndDigForNugget::Exit(Miner* pMiner)
{
  SetTextColor(FOREGROUND_BLUE | FOREGROUND_INTENSITY);
  cout << "\n" << GetNameOfEntity(pMiner->ID()) << ": " 
       << "Ah'm leavin' the goldmine with mah pockets full o' sweet gold";
}



//----------------------------------------methods for VisitBankAndDepositGold

VisitBankAndDepositGold* VisitBankAndDepositGold::Instance()
{
  static VisitBankAndDepositGold instance;

  return &instance;
}


void VisitBankAndDepositGold::Enter(Miner* pMiner)
{  
  //on entry the miner makes sure he is located at the bank
  if (pMiner->Location() != bank)
  {
    SetTextColor(FOREGROUND_RED| FOREGROUND_INTENSITY);
    cout << "\n" << GetNameOfEntity(pMiner->ID()) << ": " << "Goin' to the bank. Yes siree";

    pMiner->ChangeLocation(bank);
  }
}


void VisitBankAndDepositGold::Execute(Miner* pMiner)
{

  //deposit the gold
  pMiner->AddToWealth(pMiner->GoldCarried());
    
  pMiner->SetGoldCarried(0);

  SetTextColor(FOREGROUND_RED| FOREGROUND_INTENSITY);
  cout << "\n" << GetNameOfEntity(pMiner->ID()) << ": " 
       << "Depositing gold. Total savings now: "<< pMiner->Wealth();

  //wealthy enough to have a well earned rest?
  if (pMiner->Wealth() >= ComfortLevel)
  {
    SetTextColor(FOREGROUND_RED| FOREGROUND_INTENSITY);
    cout << "\n" << GetNameOfEntity(pMiner->ID()) << ": " 
         << "WooHoo! Rich enough for now. Back home to mah li'lle lady";
      
    pMiner->ChangeState(GoHomeAndSleepTilRested::Instance());      
  }

  //otherwise get more gold
  else 
  {
    pMiner->ChangeState(EnterMineAndDigForNugget::Instance());
  }
}


void VisitBankAndDepositGold::Exit(Miner* pMiner)
{
  SetTextColor(FOREGROUND_RED| FOREGROUND_INTENSITY);
  cout << "\n" << GetNameOfEntity(pMiner->ID()) << ": " << "Leavin' the bank";
}


//----------------------------------------methods for GoHomeAndSleepTilRested

GoHomeAndSleepTilRested* GoHomeAndSleepTilRested::Instance()
{
  static GoHomeAndSleepTilRested instance;

  return &instance;
}

void GoHomeAndSleepTilRested::Enter(Miner* pMiner)
{
  if (pMiner->Location() != shack)
  {
    SetTextColor(FOREGROUND_RED| FOREGROUND_INTENSITY);
    cout << "\n" << GetNameOfEntity(pMiner->ID()) << ": " << "Walkin' home";

    pMiner->ChangeLocation(shack); 
  }
}

void GoHomeAndSleepTilRested::Execute(Miner* pMiner)
{ 
  //if miner is not fatigued start to dig for nuggets again.
  if (!pMiner->Fatigued())
  {
    SetTextColor(FOREGROUND_GREEN | FOREGROUND_INTENSITY);
    cout << "\n" << GetNameOfEntity(pMiner->ID()) << ": " 
          << "What a God darn fantastic nap! Time to find more gold";

     pMiner->ChangeState(EnterMineAndDigForNugget::Instance());
  }
  else if (!pMiner->Ismaxfish())
  {
      SetTextColor(FOREGROUND_GREEN | FOREGROUND_INTENSITY);
      cout << "\n" << GetNameOfEntity(pMiner->ID()) << ": "
          << "not enough fish";
      pMiner->ChangeState(Fishing::Instance());
  }
  else 
  {
    //sleep
    pMiner->DecreaseFatigue();

    SetTextColor(FOREGROUND_GREEN | FOREGROUND_INTENSITY);
    cout << "\n" << GetNameOfEntity(pMiner->ID()) << ": " << "ZZZZ... ";
  } 
}

void GoHomeAndSleepTilRested::Exit(Miner* pMiner)
{ 
  SetTextColor(FOREGROUND_GREEN | FOREGROUND_INTENSITY);
  cout << "\n" << GetNameOfEntity(pMiner->ID()) << ": " << "Leaving the house";
}




//------------------------------------------------methods for QuenchThirst

QuenchThirst* QuenchThirst::Instance()
{
  static QuenchThirst instance;

  return &instance;
}

void QuenchThirst::Enter(Miner* pMiner)
{
  if (pMiner->Location() != saloon)
  {    
    pMiner->ChangeLocation(saloon);

    SetTextColor(FOREGROUND_RED| FOREGROUND_INTENSITY);
    cout << "\n" << GetNameOfEntity(pMiner->ID()) << ": " << "Boy, ah sure is thusty! Walking to the saloon";
  }
}

void QuenchThirst::Execute(Miner* pMiner)
{
   if (pMiner->Thirsty())
   {
     pMiner->BuyAndDrinkAWhiskey();

     SetTextColor(FOREGROUND_RED| FOREGROUND_INTENSITY);
     cout << "\n" << GetNameOfEntity(pMiner->ID()) << ": " << "That's mighty fine sippin liquer";

     pMiner->ChangeState(EnterMineAndDigForNugget::Instance());
  }

  else 
  {
    SetTextColor(FOREGROUND_RED| FOREGROUND_INTENSITY);
    cout << "\nERROR!\nERROR!\nERROR!";
  } 
}

void QuenchThirst::Exit(Miner* pMiner)
{ 
  SetTextColor(FOREGROUND_RED| FOREGROUND_INTENSITY);
  cout << "\n" << GetNameOfEntity(pMiner->ID()) << ": " << "Leaving the saloon, feelin' good";
}



Fishing* Fishing::Instance()
{
    static Fishing instance;

    return &instance;
}

void Fishing::Enter(Miner* pMiner)
{
    if (pMiner->Location() != fishing)
    {
        pMiner->ChangeLocation(fishing);

        SetTextColor(FOREGROUND_BLUE | FOREGROUND_INTENSITY);
        cout << "\n" << GetNameOfEntity(pMiner->ID()) << ": " << "Walking to the fishing";
    }
}

void Fishing::Execute(Miner* pMiner)
{
    if (!pMiner->Ismaxfish())
    {
        pMiner->Catchingfish();

        SetTextColor(FOREGROUND_BLUE | FOREGROUND_INTENSITY);
        cout << "\n" << GetNameOfEntity(pMiner->ID()) << ": " << "Catch the fish";
    }
    else
    {
        SetTextColor(FOREGROUND_BLUE | FOREGROUND_INTENSITY);
        cout << "\n" << GetNameOfEntity(pMiner->ID()) << ": " << "have the maximum number of fish ";
        pMiner->ChangeState(GoHomeAndSleepTilRested::Instance());
    }
}

void Fishing::Exit(Miner* pMiner)
{
    SetTextColor(FOREGROUND_BLUE | FOREGROUND_INTENSITY);
    cout << "\n" << GetNameOfEntity(pMiner->ID()) << ": " << "Leaving the fishing";
}